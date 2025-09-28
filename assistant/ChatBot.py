from groq import Groq  # Groq API
from json import load, dump, JSONDecodeError
import datetime
from dotenv import dotenv_values
from pathlib import Path

# Ensure Data directory exists
Path("Data").mkdir(parents=True, exist_ok=True)

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# System prompt
System = f"""Hello, I am {Username}. You are a very accurate AI chatbot named {Assistantname}.
*** Do not tell time unless asked. Reply only in English. ***
*** Do not provide notes, just answer the question. ***"""

SystemChatBot = [{"role": "system", "content": System}]

CHATPATH = r"Data\Data\ChatLog.json"
messages = []

# Load chat log if it exists
try:
    with open(CHATPATH, "r", encoding="utf-8") as f:
        raw = f.read().strip()
        if not raw:
            messages = []
        else:
            f.seek(0)
            messages = load(f)
            if not isinstance(messages, list):
                messages = []
except FileNotFoundError:
    with open(CHATPATH, "w", encoding="utf-8") as f:
        dump([], f)
    messages = []

def RealtimeInformation():
    now = datetime.datetime.now()
    data = (
        f"Please use this real-time information if needed:\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')} hours : {now.strftime('%M')} minutes : {now.strftime('%S')} seconds\n"
    )
    return data

def AnswerModifier(answer):
    lines = answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    return "\n".join(non_empty_lines)

def ChatBot(Query):
    """Send user query to the chatbot and return AI response"""
    try:
        # Load existing messages
        try:
            with open(CHATPATH, "r", encoding="utf-8") as f:
                raw = f.read().strip()
                if not raw:
                    message_list = []
                else:
                    f.seek(0)
                    message_list = load(f)
                    if not isinstance(message_list, list):
                        message_list = []
        except (FileNotFoundError, JSONDecodeError):
            message_list = []

        message_list.append({"role": "user", "content": Query})

        # Create completion with the new model
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + message_list,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=False
        )

        # Extract assistant response
        Answer = ""
        try:
            if hasattr(completion, "choices") and len(completion.choices) > 0:
                choice0 = completion.choices[0]
                if hasattr(choice0, "message"):
                    msg = choice0.message
                    if isinstance(msg, dict):
                        Answer = msg.get("content") or msg.get("text") or ""
                    elif hasattr(msg, "content"):
                        Answer = msg.content or ""
                elif hasattr(choice0, "text"):
                    Answer = choice0.text or ""
        except Exception:
            Answer = ""

        Answer = (Answer or "").replace("</s>", " ").strip()

        message_list.append({"role": "assistant", "content": Answer})

        with open(CHATPATH, "w", encoding="utf-8") as f:
            dump(message_list, f, indent=4, ensure_ascii=False)

        return AnswerModifier(Answer)
    except Exception as e:
        print(f"Error: {e}")
        try:
            with open(CHATPATH, "w", encoding="utf-8") as f:
                dump([], f, indent=4)
        except Exception:
            pass
        return "Sorry — an internal error occurred and the chat log was reset."

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(ChatBot(user_input))
