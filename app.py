from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os, json
from dotenv import load_dotenv
from groq import Groq
from pdf_utils import extract_text_from_pdf

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🔹 SAFE JSON
def safe_json(text):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except:
        return {}


# 🔹 NORMALIZATION (IMPORTANT FIX)
def normalize(skills):
    mapping = {
        "react.js": "react",
        "vue.js": "vue",
        "node.js": "node",
        "postgres": "postgresql",
        "aws/azure": "aws"
    }

    return list(set([mapping.get(s.lower().strip(), s.lower().strip()) for s in skills]))


# 🔹 REMOVE GARBAGE
def clean_skills(skills):
    cleaned = []
    for s in skills:
        s = s.lower().strip()

        if len(s) > 20:
            continue

        if len(s.split()) > 2:
            continue

        cleaned.append(s)

    return list(set(cleaned))


# 🔹 AI SKILL EXTRACTION (NO MANUAL DB)
def extract_skills(text):
    prompt = f"""
Extract ONLY technical skills.

Return JSON:
{{"skills":[]}}

Rules:
- Only tools/technologies (python, react, aws, docker)
- No sentences
- No soft skills
- No long phrases

Text:
{text}
"""

    try:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        data = safe_json(res.choices[0].message.content)
        return normalize(clean_skills(data.get("skills", [])))

    except Exception as e:
        print("Skill error:", e)
        return []


# 🔹 OR LOGIC (CRITICAL FIX)
def apply_or_logic(matched, missing):
    groups = [
        ["react", "vue", "angular"]
    ]

    for group in groups:
        if any(skill in matched for skill in group):
            missing = [m for m in missing if m not in group]

    return missing


# 🔹 AI ANALYSIS
def analyze_ai(matched, missing):
    prompt = f"""
You are a recruiter.

Matched skills: {matched}
Missing skills: {missing}

Return JSON:
{{
"strengths":[],
"suggestions":[],
"courses":[{{"name":"","link":""}}],
"summary":""
}}

Rules:
- Suggestions ONLY for missing skills
- Courses ONLY for missing skills
- Do NOT include unrelated topics like AI, IoT
"""

    try:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return safe_json(res.choices[0].message.content)

    except Exception as e:
        print("AI error:", e)
        return {}


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        file = request.files.get('file')
        jd = request.form.get("job_description")

        if not file or not jd:
            return jsonify({"error": "Missing input"}), 400

        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        resume_text = extract_text_from_pdf(path)

        # 🔥 SKILLS
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(jd)

        matched = list(set(resume_skills) & set(job_skills))
        missing = list(set(job_skills) - set(resume_skills))

        # 🔥 FIX OR CONDITIONS
        missing = apply_or_logic(matched, missing)

        # 🔥 SCORE
        score = int((len(matched) / len(job_skills)) * 100) if job_skills else 0

        # 🤖 AI REASONING
        ai_data = analyze_ai(matched, missing)

        return jsonify({
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "strengths": ai_data.get("strengths", []),
            "suggestions": ai_data.get("suggestions", []),
            "courses": ai_data.get("courses", []),
            "summary": ai_data.get("summary", "")
        })

    except Exception as e:
        print("FINAL ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)