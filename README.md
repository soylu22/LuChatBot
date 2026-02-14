# LU ChatBot 🤖

LU is a powerful RAG (Retrieval-Augmented Generation) chatbot built with **Django** and powered by **Google Gemini AI**. It uses **PostgreSQL** with the **pgvector** extension to store and retrieve knowledge efficiently, providing context-aware responses.

## 🚀 Features

- **Contextual Responses:** Answers questions based on ingested knowledge.
- **Data Ingestion:** Easily ingest text content into the knowledge base.
- **Chat History:** Securely saves and retrieves user chat sessions.
- **Modern UI:** Clean, responsive frontend for seamless interaction.
- **Secure Authentication:** JWT-based user signup and login.

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Frontend:** Vanilla HTML, CSS, JavaScript
- **Database:** PostgreSQL + [pgvector](https://github.com/pgvector/pgvector)
- **AI Models:** 
  - `gemini-embedding-001` (Embeddings)
  - `gemini-2.5-flash` (LLM)

---

## ⚙️ Setup Instructions

### 1. Prerequisites
- Python 3.10+
- PostgreSQL (with `pgvector` installed)
- Google Gemini API Key

### 2. Backend Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/soylu22/LuChatBot.git
   cd LuChatBot/backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the `backend/` directory:
   ```env
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=127.0.0.1
   DB_PORT=5432
   GOOGLE_API_KEY=your_gemini_api_key
   ```

5. **Database Setup:**
   Ensure PostgreSQL is running and the `pgvector` extension is enabled in your database:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

6. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Start the Server:**
   ```bash
   python manage.py runserver
   ```

### 3. Frontend Setup
The frontend is built with vanilla web technologies. You can serve it using any local server or simply open `frontend/index.html` in your browser.

- To run with Live Server (VS Code), right-click `index.html` and select **Open with Live Server**.
- Ensure the backend is running at `http://localhost:8000`.

---

## 📖 Usage

1. **Signup/Login:** Create an account to start chatting.
2. **Ingest Knowledge:** Use the Admin dashboard (`admin.html`) to ingest text data that LU will use as context.
3. **Chat:** Ask LU anything! It will retrieve relevant info from your ingested data and generate a response.

## 📂 Project Structure

```text
ChatBot/
├── backend/            # Django Application
│   ├── chat/           # Chat & RAG Logic
│   ├── lu_backend/      # Project Settings
│   └── manage.py
├── frontend/           # Web Assets
│   ├── css/
│   ├── js/
│   └── *.html
└── README.md
```

---

*Developed by [soylu22](https://github.com/soylu22)*