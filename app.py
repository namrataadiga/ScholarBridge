import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Hardcoded API Key to ensure it works instantly during your presentation tomorrow
# Change line 10 in app.py to this:
import os

# 1. First, check if Render has the key stored in cloud memory
api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

# 2. EMERGENCY LOCAL FALLBACK: If it's not found on the server, use your working key text string
if not api_key:
    api_key = "AQ.Ab8RN6JFbcli5CRqRAA8xkdVllZQAfWI6OIOn7whu-4YMn8WxQ"

# 3. Explicitly initialize the client using the resolved key string
client = genai.Client(api_key=api_key)

# System instructions to give Scholar Bridge its personality and boundaries
SYSTEM_INSTRUCTION = """
You are Scholar Bridge, an empathetic, supportive, and knowledgeable AI assistant dedicated to helping underprivileged students find educational resources, courses, diplomas, scholarships, and career paths.
- Keep your language simple, encouraging, and completely free of academic jargon.
- Prioritize affordable, free, vocational, or government-funded educational tracks.
- Provide clear, step-by-step guidance on how to apply for scholarships or admissions.
- If a student asks something outside of education or career guidance, gently redirect them back to their educational goals.
"""

@app.route("/")
def home():
    # Renders the index.html file from your templates folder
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Requesting response from Gemini 2.5 Flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
            )
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"reply": "I'm having a little trouble connecting right now. Please try asking again in a moment!"}), 500

if __name__ == "__main__":
    app.run(debug=True)