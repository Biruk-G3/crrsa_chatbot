from django.shortcuts import render
import json
import os
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .ai import ask_ai

def home(request):
    return HttpResponse("Telegram bot is running")

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Telegram message
        message = data.get("message")
        if message:
            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            # ask AI
            reply = ask_ai(text)

            # send reply back to Telegram
            
            token = os.environ.get("TELEGRAM_BOT_TOKEN")
            url = f"https://api.telegram.org/bot{8664683565:AAHeE1QgJB9C0UgPinBGi2hLfxkUojTh01s}/sendMessage"
            requests.post(url, json={"chat_id": chat_id, "text": reply})

    return JsonResponse({"status": "ok"})
