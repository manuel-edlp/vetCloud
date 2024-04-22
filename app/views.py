from django.shortcuts import render
from .models import Client

def home(request):
    return render(request, "home.html")

def clients_repository(request):
    clients = Client.objects.all()
    return render(request, "clients/repository.html", { "clients": clients })