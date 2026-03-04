from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)  # for testing
    return JsonResponse({"status": "ok"})
