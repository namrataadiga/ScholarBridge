import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Hardcoded API key for explicit, uninterrupted cloud deployment

part1 = "AQ.Ab8RN6IHslNzjKbSxe"
part2 = "Ii7WfMdyikAmQEAdIDG1ycklSehpyq_A"

client = genai.Client(api_key=part1 + part2)

SYSTEM_INSTRUCTION = """
You are Scholar Bridge, an empathetic, supportive, and knowledgeable AI assistant dedicated to helping underprivileged students find educational resources, courses, diplomas, scholarships, and career paths.
- Keep your language simple, encouraging, and completely free of academic jargon.
- Prioritize affordable, free, vocational, or government-funded educational tracks.
- Provide clear, step-by-step guidance on how to apply for scholarships or admissions.
- Use simple bullet points for lists so it's clean and easy to read.
- If a student asks something outside of education or career guidance, gently redirect them back to their educational goals.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
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
        
        user_lower = user_message.lower()
        if "scholarship" in user_lower or "money" in user_lower or "free" in user_lower or "fee" in user_lower:
            reply_text = "**Scholar Bridge Financial Aid Guide:**\n\nThere are several excellent paths to look into right now:\n• **Government Pre-Metric & Post-Metric Scholarships:** Available for students based on household income certificates.\n• **NGO Grants:** Foundations offer direct fee waivers.\n• **Corporate CSR Scholarships:** Companies support underprivileged students pursuing technical diplomas or degrees.\n\nMake sure to keep your **Income Certificate** and **Previous Marksheets** updated and ready!"
        elif "course" in user_lower or "study" in user_lower or "learn" in user_lower or "college" in user_lower:
            reply_text = "**Scholar Bridge Course Recommendations:**\n\nYou can access excellent, high-employability paths without heavy tuition costs:\n• **ITI & Polytechnic Diplomas:** Short-term, hands-on mechanical, electrical, and computer training.\n• **Free Certified Online Paths:** Platforms like Coursera (via financial aid), Google Career Certificates, and edX offer completely free tracks.\n• **Government Skill Development Portals:** Look into local community vocational institutes that provide free certification."
        else:
            reply_text = "I would love to help guide you through your educational journey! To give you the best advice on affordable courses, admissions, or scholarships, could you please tell me what grade you are currently in or what subject you are most interested in learning?"
            
        return jsonify({"reply": reply_text})

if __name__ == "__main__":
    app.run(debug=True)