from django.conf import settings
from django.shortcuts import render
import json
from django.http import JsonResponse
import os

# management = os.path.join(settings.MEDIA_ROOT, 'management.json')

def hello(request):
    return render(request, 'homepage.html')


def display_json_data(request):
    try:
        json_file_path = os.path.join(settings.MEDIA_ROOT, "management.json")
        with open(json_file_path,'r') as  json_file:
            data = json.load(json_file) 
    except FileNotFoundError:
        data={}
        
    # return JsonResponse(data)
    return render(request, "homepage.html",{"json_data": data})
    




