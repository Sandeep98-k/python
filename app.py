from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os
import re

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Skills database (you can extend this)
SKILLS = [
    "python", "sql", "excel", "power bi", "machine learning",
    "flask", "html", "css", "javascript", "data analysis",
    "pandas", "numpy", "api", "git"
]

def extract_text_from_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text().lower()
    return text

def analyze_resume(text):
    matched = []
    missing = []

    for skill in SKILLS:
        if skill in text:
            matched.append(skill)
        else:
            missing.append(skill)

    ats_score = int((len(matched) / len(SKILLS)) * 100)

    suggestions = [
        "Add more technical skills",
        "Include projects section",
        "Mention internships if any",
        "Use strong action verbs"
    ]

    return {
        "ats": ats_score,
        "matched": matched,
        "missing": missing,
        "extra": [],
        "suggestions": suggestions
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files.get("resume")

        if file and file.filename.endswith(".pdf"):
            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)

            text = extract_text_from_pdf(path)
            result = analyze_resume(text)

    return render_template("image.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
