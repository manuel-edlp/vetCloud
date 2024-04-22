from django.shortcuts import render, redirect, reverse
from .models import Client


def home(request):
    return render(request, "home.html")


def clients_repository(request):
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients})


def validate_client(data):
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


def save_client(client_data):
    errors = validate_client(client_data)

    if len(errors.keys()) > 0:
        return False, errors

    Client.objects.create(
        name=client_data.get("name"),
        phone=client_data.get("phone"),
        email=client_data.get("email"),
        address=client_data.get("address"),
    )

    return True, None


def clients_form(request):
    if request.method == "POST":
        saved, errors = save_client(request.POST)

        if saved:
            return redirect(reverse("clients_repo"))

        return render(
            request, "clients/form.html", {"errors": errors, "data": request.POST}
        )

    return render(request, "clients/form.html")
