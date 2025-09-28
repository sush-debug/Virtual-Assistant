import pygame
import random
import asyncio
import edge_tts
import os
import uuid
from dotenv import dotenv_values

# Load voice from .env file
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistanceVoice")

# Data folder for speech files
DATA_FOLDER = r"C:\Users\saraw\OneDrive\Desktop\virtual_assistant\Data"
os.makedirs(DATA_FOLDER, exist_ok=True)  # ensure folder exists


# -------- Async function to generate speech file --------
async def TextToAudioFile(text: str) -> str:
    # Unique filename for each playback
    file_path = os.path.join(DATA_FOLDER, f"Speech_{uuid.uuid4().hex}.mp3")
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)
    return file_path


# -------- Function to play TTS --------
def TTS(Text, func=lambda r=None: True):
    file_path = None
    try:
        # Generate speech file
        file_path = asyncio.run(TextToAudioFile(Text))

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        # Keep playing until done
        while pygame.mixer.music.get_busy():
            if func() is False:
                break
            pygame.time.Clock().tick(10)

        return True

    except Exception as e:
        print(f"Error in TTS: {e}")

    finally:
        try:
            func(False)
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.quit()

            # Clean up speech file
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

        except Exception as e:
            print(f"error in finally block: {e}")


# -------- Main TextToSpeech logic with splitting --------
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")

    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    # If text is too long → speak first part + random polite response
    if len(Data) > 4 and len(Text) >= 250:
        TTS(" ".join(Text.split(".")[0:2]) + " . " + random.choice(responses), func)
    else:
        TTS(Text, func)


# -------- For testing --------
if __name__ == "__main__":
    while True:
        user_input = input("Enter your text (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        TextToSpeech(user_input)
