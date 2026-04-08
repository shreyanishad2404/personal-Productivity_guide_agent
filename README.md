

---

# 🤖 Mini Jarvis - Personal Productivity AI

An intelligent **AI-powered productivity assistant** that helps you manage tasks, save notes, and organize your daily workflow using a multi-agent architecture.

---

# 🚀 Features

* 💬 Natural language conversation
* 📋 Task management (add, view, complete tasks)
* 📝 Notes storage and retrieval
* 🧠 Smart productivity assistant (Mini Jarvis personality)
* ⚡ Fast API using FastAPI
* ☁️ Deployable on Google Cloud Run
* 🔗 Multi-agent architecture (Google ADK)
* 📦 Easy-to-extend tools system

---

# 🛠️ Tech Stack

* Python
* FastAPI
* Google ADK
* Google Cloud Datastore
* Uvicorn
* Pydantic
  <img width="1910" height="922" alt="image" src="https://github.com/user-attachments/assets/e9385713-586d-4ada-98af-e3ebdf7b62cf" />


---

# 📂 Project Structure

```
.
├── agent.py              # Main multi-agent logic
├── requirements.txt      # Dependencies
├── .env                  # Environment variables
├── README.md             # Project documentation
```

---

# ⚙️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/mini-jarvis-agent.git
cd mini-jarvis-agent
pip install -r requirements.txt
```

---

# ▶️ Run Locally

```bash
uvicorn agent:app --reload
```

👉 Server will start at:

```
http://localhost:8080
```

---

# 📡 API Endpoint

### POST `/api/v1/jarvis/chat`

#### Request:

```json
{
  "prompt": "Add task to study AI"
}
```

#### Response:

```json
{
  "status": "success",
  "reply": "✅ Task added successfully."
}
```

---

# ☁️ Deploy to Cloud Run

```bash
uvx --from google-adk==1.14.0 \
adk deploy cloud_run \
  --project=$PROJECT_ID \
  --region=us-central1 \
  --service_name=mini-jarvis \
  --with_ui \
  . \
  -- \
  --service-account=$SERVICE_ACCOUNT
```

---

# 🔐 Environment Variables

Create a `.env` file:

```env
PROJECT_ID=multi-agents-project
MODEL=gemini-1.5-flash
GOOGLE_APPLICATION_CREDENTIALS=path-to-key.json
```

---

# 📌 Usage

1. Start the server
2. Send API request (Postman / curl)
3. Chat with Mini Jarvis 🤖

---

# 💬 Example Commands

* “Add task to study AI”
* “Show my tasks”
* “Complete task 1”
* “Save note about project ideas”
* “Plan my day”

---

# 🧠 How It Works

* **Root Agent** → receives user input
* **Workflow Agent** → processes request
* **Tools (MCP)** → perform actions (task, notes)
* **Datastore** → stores data

---

# 🚀 Future Improvements

* ⏰ Reminder system
* 📅 Calendar integration
* 🌐 Frontend dashboard
* 🎤 Voice assistant
* 🤖 Advanced planning agent

---

# 👩‍💻 Author

**Shreya Nishad**

---

# ⭐ Support

If you like this project:

* ⭐ Star the repo
* 🍴 Fork it
* 🚀 Build on top of it

---
