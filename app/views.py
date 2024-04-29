from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Client
from .models import Provider
from .models import Veterinary


def home(request):
    return render(request, "home.html")


def clients_repository(request):
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients})


def clients_form(request, id=None):
    if request.method == "POST":
        client_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if client_id == "":
            saved, errors = Client.save_client(request.POST)
        else:
            client = get_object_or_404(Client, pk=client_id)
            client.update_client(request.POST)

        if saved:
            return redirect(reverse("clients_repo"))

        return render(
            request, "clients/form.html", {"errors": errors, "client": request.POST}
        )

    client = None
    if id is not None:
        client = get_object_or_404(Client, pk=id)

    return render(request, "clients/form.html", {"client": client})


def clients_delete(request):
    client_id = request.POST.get("client_id")
    client = get_object_or_404(Client, pk=int(client_id))
    client.delete()

    return redirect(reverse("clients_repo"))

# Proveedor
def provider_repository(request):
    providers = Provider.objects.all()
    return render(request, "providers/repository.html", {"providers": providers})


def provider_form(request, id=None):
    if request.method == "POST":
        provider_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if provider_id == "":
            saved, errors = Provider.save_provider(request.POST)
        else:
            provider = get_object_or_404(Provider, pk=provider_id)
            provider.update_provider(request.POST)

        if saved:
            return redirect(reverse("provider_repo"))

        return render(
            request, "providers/form.html", {"errors": errors, "provider": request.POST}
        )

    provider = None
    if id is not None:
        provider = get_object_or_404(Provider, pk=id)

    return render(request, "providers/form.html", {"provider": provider})


def provider_delete(request):
    provider_id = request.POST.get("provider_id")
    provider = get_object_or_404(Provider, pk=int(provider_id))
    provider.delete()

    return redirect(reverse("provider_repo"))

#Veterinario

def veterinary_repository(request):
    veterinary = Veterinary.objects.all()
    return render(request, "veterinary/repository.html", {"veterinary": veterinary})


def veterinary_form(request, id=None):
    if request.method == "POST":
        veterinary_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if veterinary_id == "":
            saved, errors = Veterinary.save_veterinary(request.POST)
        else:
            veterinary = get_object_or_404(Veterinary, pk=veterinary_id)
            veterinary.update_veterinary(request.POST)

        if saved:
            return redirect(reverse("veterinary_repo"))

        return render(
            request, "veterinarys/form.html", {"errors": errors, "veterinary": request.POST}
        )

    veterinary = None
    if id is not None:
        veterinary = get_object_or_404(Veterinary, pk=id)

    return render(request, "veterinary/form.html", {"veterinary": veterinary})


def veterinary_delete(request):
    veterinary_id = request.POST.get("veterinary_id")
    veterinary = get_object_or_404(Veterinary, pk=int(veterinary_id))
    veterinary.delete()

    return redirect(reverse("veterinary_repo"))