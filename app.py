from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask (__name__)

client = genai.Client(api_key=os.getenv("api"))

@app.route("/", methods=["GET", "POST"])

def index():
    quotes = []
    
    if request.method == "POST":
        topic = request.form["topic"]
        
        prompt = f"""
        Generate 5 short inspirational quotes about (topic).
        Each quote should be on a new line.
        """
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt
        )
        
        quotes = response.text.strip().split("\n")
            
    return render_template("index.html", quotes=quotes)


if name == "__main__":
    app.run (debug=True)
