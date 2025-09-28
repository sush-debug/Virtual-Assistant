# FRIDAY - Virtual Assistant 🤖  

FRIDAY is a Virtual Assistant built using **Python, Django, HTML, CSS, and JavaScript**.  
It automates tasks, responds to **voice/text commands**, generates **AI images**, performs searches, and provides real-time assistance.  

![Python](https://img.shields.io/badge/Python-3.10-blue)  
![Django](https://img.shields.io/badge/Django-4.x-green)  
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)  

---

## 🚀 Features  

- 🎙️ **Voice & Text Interaction** – Communicate with FRIDAY using natural language.  
- ⚡ **Task Automation** – Open apps, perform searches, set reminders, and execute system commands.  
- 🗣️ **Speech-to-Text (STT) & Text-to-Speech (TTS)** – Converts speech into text and responds with natural voice.   
- 🔎 **YouTube & Web Search** – Search and fetch results directly.  
- 🤖 **Smart Replies** – Context-aware responses for smooth interaction.  
- 🔐 **Authentication System** – User login/signup with data stored in database.  
- 💾 **Database Integration** – Stores user data, messages, and activity logs.  
- 🌍 **Cross-Platform Deployment** – Deploy on [PythonAnywhere](https://www.pythonanywhere.com/), [Render](https://render.com/), [Heroku](https://www.heroku.com/), or [Vercel](https://vercel.com/).  

---

## 🛠️ Tech Stack  

- **Frontend**: HTML, CSS, JavaScript (Bootstrap/Tailwind optional)  
- **Backend**: Django (Python)  
- **Database**: SQLite / PostgreSQL  
- **APIs & Libraries**:  
  - Speech Recognition  
  - Text-to-Speech (`pyttsx3` / `gTTS`)  
  - OpenAI / Hugging Face APIs (for AI responses & image generation)  
  - Django REST Framework  

---

## ⚙️ Installation & Setup  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/virtual-assistant.git
   cd virtual-assistant
Create virtual environment & install dependencies

bash
Copy code
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
Setup environment variables
Create a .env file in the project root:

ini
Copy code
SECRET_KEY=your_secret_key
DEBUG=True
OPENAI_API_KEY=your_api_key
Run migrations & start server

bash
Copy code
python manage.py migrate
python manage.py runserver