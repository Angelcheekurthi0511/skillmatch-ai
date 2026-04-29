# 🚀 SkillMatch AI – Resume Analyzer

An AI-powered web application that analyzes resumes against job descriptions and provides skill match scores, missing skills, and actionable recommendations using Large Language Models (LLMs).

---

## 🔥 Features

* 📄 Upload Resume (PDF)
* 🧠 AI-based Skill Extraction (No manual database)
* 🎯 Match Score Calculation
* ✅ Matched & ❌ Missing Skills Detection
* 💪 Strengths & 📈 Improvement Suggestions
* 🎓 Recommended Courses with links
* ⚡ Real-time analysis using Groq API

---

## 🌐 Live Demo

👉 https://skillmatch-ai-n294.onrender.com/

---

## 🛠 Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Flask (Python)
* **AI Model:** Groq LLM API
* **PDF Parsing:** PyMuPDF / PyPDF2
* **Deployment:** Render

---

## ⚙️ How It Works

1. User uploads a resume (PDF)
2. User pastes a job description
3. Backend extracts text from PDF
4. LLM analyzes both inputs
5. System generates:

   * Match score
   * Matched skills
   * Missing skills
   * Suggestions & courses
6. Results are displayed instantly

---

## 📁 Project Structure

```
skillmatch-ai/
│
├── app.py
├── pdf_utils.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   └── index.html
│
├── uploads/




---

## 🚀 Deployment

Deployed on **Render**

* Build Command:

```
pip install -r requirements.txt
```

* Start Command:

```
gunicorn app:app
```

---

## 📌 Future Improvements

* 📊 Skill gap visualization (charts)
* 📄 Downloadable PDF report
* 🎤 AI interview simulator integration
* 🌐 Multi-language support

---

## 👨‍💻 Author

**Angel Cheekurthi**
B.Tech – AI & Data Science

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
