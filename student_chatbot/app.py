from flask import Flask, request, jsonify, render_template
from google import genai
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)

# Load local FAQ
with open("faq.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# In-memory context per session
conversation_context = {}

# Simple dynamic quick replies based on user input keywords
def get_quick_replies(query):
    query_lower = query.lower()
    buttons = []
    if "admission" in query_lower:
        buttons = ["Admission 📚", "Eligibility ✅"]
    elif "exam" in query_lower:
        buttons = ["Exam Schedule 📝", "Exam Fees 💰"]
    elif "placement" in query_lower:
        buttons = ["Placement Companies 💼", "Eligibility Criteria 🎯"]
    elif "hostel" in query_lower:
        buttons = ["Hostel Info 🏠", "Mess Menu 🍴"]
    else:
        buttons = ["Admissions 📚", "Exam Schedule 📝", "Placements 💼", "Hostel Info 🏠"]
    return buttons

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
        # Call Gemini AI
        try:
            prev_context = conversation_context.get(session_id, "")
            combined_input = f"{prev_context}\nUser: {user_query}\nBot:"
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=combined_input
            )
            answer = response.text
            # Update context
            conversation_context[session_id] = combined_input + " " + answer
        except Exception as e:
            print("Error:", e)
            answer = "Sorry, I couldn't process your request. Please try again."

    # Return answer and quick replies
    quick_buttons = get_quick_replies(user_query)
    return jsonify({"answer": answer, "quick_replies": quick_buttons})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
