from flask import Flask, request, jsonify, render_template
from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)

with open("faq.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

conversation_history = {}

SYSTEM_PROMPT = """You are a helpful college student assistant named Campus AI. 
You assist students with questions about admissions, exams, placements, hostel info, 
scholarships, and general campus life. Be concise, friendly, and accurate. 
If you don't know something specific about the college, say so honestly and suggest 
the student visit the official portal or contact the relevant department."""

def get_quick_replies(query):
    q = query.lower()
    if "admission" in q or "apply" in q:
        return ["Eligibility ✅", "Documents needed 📄", "Application fees 💰"]
    elif "exam" in q:
        return ["Exam fees 💰", "Admit card 🪪", "Results 📊"]
    elif "placement" in q or "compan" in q:
        return ["Eligibility criteria 🎯", "Internships 🔬", "Package details 💼"]
    elif "hostel" in q or "mess" in q:
        return ["Mess menu 🍴", "Hostel fees 💰", "Warden contact 📞"]
    else:
        return ["Admissions 🎓", "Exam Schedule 📝", "Placements 💼"]

def check_faq(query):
    query_lower = query.lower()
    for item in faq_data:
        for q in item["questions"]:
            if q.lower() in query_lower:
                return item["answer"]
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query")
    session_id = request.json.get("session_id", "default")

    # Check FAQ first
    answer = check_faq(user_query)

    if answer is None:
        if session_id not in conversation_history:
            conversation_history[session_id] = []

        # Add user message
        conversation_history[session_id].append({
            "role": "user",
            "content": user_query
        })

        # Keep last 10 messages
        history = conversation_history[session_id][-10:]

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *history
                ],
                max_tokens=512,
                temperature=0.7
            )
            answer = response.choices[0].message.content

            # Save assistant response
            conversation_history[session_id].append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            print("Groq API Error:", type(e).__name__, str(e))
            answer = "Sorry, I couldn't process your request right now. Please try again shortly."

    quick_buttons = get_quick_replies(user_query)
    return jsonify({"answer": answer, "quick_replies": quick_buttons})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)