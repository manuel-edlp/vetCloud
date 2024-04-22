from django.shortcuts import render, redirect, reverse
from .models import Client


def home(request):
    return render(request, "home.html")


def clients_repository(request):
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients})


def clients_form(request):
    if request.method == "POST":
        saved, errors = Client.save_client(request.POST)

        if saved:
            return redirect(reverse("clients_repo"))

        return render(
            request, "clients/form.html", {"errors": errors, "data": request.POST}
        )

    return render(request, "clients/form.html")
