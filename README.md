# 🎓 Campus AI — Student Assistant Chatbot

A conversational AI chatbot that helps college students get instant answers about admissions, exams, placements, hostel info, and more.

## 🚀 Live Demo
[Click here to try it](https://student-assistant-chatbot-2k4t.onrender.com)

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **AI:** Groq API (Llama 3.3 70B)
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Render

## ✨ Features
- FAQ-first architecture for instant responses without hitting the AI API
- Multi-turn conversation memory per session
- Dynamic quick reply buttons based on context
- Clean, responsive chat UI with typing indicators
- Graceful fallback handling for API errors

## 🏗️ Architecture
```
User Message
     ↓
FAQ Match? → Yes → Return instant answer
     ↓ No
Groq AI API (Llama 3.3) with session history
     ↓
Response + Dynamic Quick Replies
```

## ⚙️ Run Locally

1. Clone the repo
```bash
git clone https://github.com/bhanuchukka2005-spec/Student-assistant-chatbot.git
cd Student-assistant-chatbot
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a `.env` file
```
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the app
```bash
python app.py
```

5. Open http://localhost:5000

## 📁 Project Structure
```
student_chatbot/
├── app.py           # Flask backend + API integration
├── faq.json         # Local FAQ data
├── requirements.txt
├── Procfile         # For Render deployment
├── .gitignore
└── templates/
    └── index.html   # Chat UI
```

## 🔮 Planned Improvements
- Vector search using ChromaDB for smarter FAQ matching
- Persistent chat history with SQLite
- Admin dashboard to view common student queries
- RAG pipeline for college document Q&A

## 👤 Author
**Bhanu** — B.Tech CSE Student at Presidency University
[LinkedIn](https://www.linkedin.com/in/chukka-bhanu-prakash) · [GitHub](https://github.com/bhanuchukka2005-spec)
