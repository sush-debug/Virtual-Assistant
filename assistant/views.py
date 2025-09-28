from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .ChatBot import ChatBot
from .SpeechToText import SpeechRecognition
from .TextToSpeech import TextToSpeech
from .Automation import Automation
import asyncio


# Render pages
def index(request):
    return render(request, 'assistant/index.html')

def chats(request):
    return render(request, 'assistant/chats.html')


# Chat API (text → response)
@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not user_message.strip():
                return JsonResponse({"response": "⚠️ Please enter a valid message."})

            # Call chatbot
            bot_reply = ChatBot(user_message)

            return JsonResponse({"response": bot_reply})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# Speech to Text
@csrf_exempt
def stt_view(request):
    if request.method == "POST":
        try:
            text = SpeechRecognition()
            return JsonResponse({"text": text})
        except Exception as e:
            return JsonResponse({"text": "", "error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# Text to Speech
@csrf_exempt
def tts_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "")
            TextToSpeech(text)  # play audio
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)



# This view will accept a list of commands from frontend
@csrf_exempt
def automation_view(request):
    """
    Handles automation tasks like opening apps, YouTube search, etc.
    Example: /automation/?commands[]=open chrome&commands[]=youtube search ai
    """
    # Get commands from query params
    commands = request.GET.getlist("commands[]")

    if not commands:
        return JsonResponse({"error": "No commands provided"}, status=400)

    try:
        # Run the async Automation function
        result = asyncio.run(Automation(commands))

        return JsonResponse({
            "success": True,
            "executed": commands,
            "result": result
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)