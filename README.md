# 📬 Email Daily Digest Bot

A Python script that fetches unread emails from Gmail, summarizes them using OpenAI, and sends a compact daily digest to your inbox.

---

## ✨ Features

- ✅ Fetches unread emails from the past 24 hours
- 🤖 Summarizes email content using OpenAI
- 📦 Splits summaries into digestible chunks
- 📧 Sends a clean, concise daily summary to your Gmail

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/email-daily-digest.git
cd email-daily-digest
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Google API Credentials

- Go to Google Cloud Console
- Enable the Gmail API
- Download `credentials.json` and place it in the project root
- On first run, the script will generate `token.json` after authentication

### 5. Set Up .env File (Recommended)

Create a `.env` file with your OpenAI key:

```env
OPENAI_API_KEY=your_openai_api_key
```

Update the script to use this key if not already.

---

## 🚀 Running the Script

```bash
python daily_digest.py
```

You’ll see progress logs like:

```
🔐 Authenticating...
📥 Fetching unread emails...
📦 Splitting into chunks...
🧠 Summarizing chunk 1...
📤 Sending summary email...
✅ Done!
```

---

## 📁 .gitignore

This project excludes sensitive files:

```
venv/
token.json
credentials.json
token.pickle
token.pkl
.env
__pycache__/
```

---

## 🤝 Contributions

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 🛡 Security

⚠️ Never commit API keys or tokens. GitHub will block such pushes for your safety. Use `.env` files or secret managers.
