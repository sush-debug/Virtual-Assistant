# Standard library imports
import os
import subprocess
import asyncio
import webbrowser
from webbrowser import open as webopen
import keyboard

# Third-party library imports
from AppOpener import close, open as appopen
from pywhatkit import search
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import requests

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
client = Groq(api_key=GroqAPIKey)

# Ensure Data folder exists (deployment-friendly)
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data")
os.makedirs(DATA_FOLDER, exist_ok=True)

# Predefined classes and user agent
classes = ["zCubWf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_vk FzWSb Ywphnf",
           "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "OSuR6d LTKOO",
           "vlzY6d", "webanswers-webanswer_table__webanswers-table", "dDoNo ikb48b gsrt",
           "sXLaOe", "LWKfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
headers = {"user-agent": useragent}

# Professional responses
professional_responses = [
    "Your satisfaction is my top priority: feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need - don't hesitate to ask."
]

# Chatbot messages
messages = []
SystemChatBot = [{"role":"system", "content": f"Hello, I am {env_vars.get('Username','User')}, you're a content writer. You must write content like letters, codes, applications, essays, notes, songs, poems, jokes etc."}]

# ----------------------------
# Core Functions
# ----------------------------

def GoogleSearch(Topic):
    search(Topic)
    return f"Searched Google for '{Topic}'"

def Content(Topic):

    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user","content": prompt})

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        answer = ""
        for chunk in completion:
            try:
                delta = chunk.choices[0].delta
                content = getattr(delta, 'content', None)
                if content is None and isinstance(delta, dict):
                    content = delta.get('content')
            except Exception:
                content = None

            if content:
                answer += content

        answer = answer.replace("</s>", " ")
        messages.append({"role": "assistant", "content": answer})
        return answer

    Topic = Topic.replace("Content", " ").strip()
    ContentByAI = ContentWriterAI(Topic)

    # Save content to file in DATA_FOLDER
    file_name = f"{Topic.lower().replace(' ', '_')}.txt"
    file_path = os.path.join(DATA_FOLDER, file_name)

    with open(file_path, "w", encoding="UTF-8") as f:
        f.write(ContentByAI)

    OpenNotepad(file_path)
    return f"Created and opened content file for '{Topic}'"

def YouTubeSearch(Topic):
    url = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(url)
    return f"Opened YouTube search for '{Topic}'"

def OpenApp(app, sess=None):
    if sess is None:
        sess = requests.session()

    try:
        appopen(app, match_closest=False, output=True, throw_error=True)
        return f"Opened {app}"
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UNckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            response = sess.get(url, headers=headers)
            return response.text if response.status_code == 200 else None

        html = search_google(app)
        if html:
            extracted = extract_links(html)
            if extracted:
                webopen(extracted[0])
                return f"Searched online and opened {app}"
        return f"Could not open {app}"

def CloseApp(app):
    if "chrome" in app:
        return "Refused to close Chrome"
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return f"Closed {app}"
        except:
            return f"Could not close {app}"

def System(command):
    def mute(): keyboard.press_and_release("volume mute")
    def unmute(): keyboard.press_and_release("volume unmute")
    def volume_up(): keyboard.press_and_release("volume up")
    def volume_down(): keyboard.press_and_release("volume down")

    if command == "mute": mute(); return "Muted system volume"
    if command == "unmute": unmute(); return "Unmuted system volume"
    if command == "volume up": volume_up(); return "Increased system volume"
    if command == "volume down": volume_down(); return "Decreased system volume"
    return f"Unknown system command: {command}"

# ----------------------------
# Async Command Execution
# ----------------------------

async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        command = command.strip().lower()
        if command.startswith("open "):
            funcs.append(asyncio.to_thread(OpenApp, command.removeprefix("open").strip()))
        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, command.removeprefix("close").strip()))
        elif command.startswith("content "):
            funcs.append(asyncio.to_thread(Content, command.removeprefix("content").strip()))
        elif command.startswith("youtube search"):
            funcs.append(asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search").strip()))
        elif command.startswith("google search"):
            funcs.append(asyncio.to_thread(GoogleSearch, command.removeprefix("google search").strip()))
        elif command.startswith("system "):
            arg = command.removeprefix("system ").strip()
            funcs.append(asyncio.to_thread(System, arg))
        else:
            funcs.append(asyncio.to_thread(lambda: f"No function found for: {command}"))

    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

async def Automation(commands: list[str]):
    results = []
    async for result in TranslateAndExecute(commands):
        results.append(result)
    return results
