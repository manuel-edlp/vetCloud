from django.urls import reverse

links = [
    {"label": "Home", "href": reverse("home"), "icon": "bi bi-house-door"},
    {"label": "Clientes", "href": reverse("clients_repo"), "icon": "bi bi-people"},
    {"label": "Proveedores", "href": reverse("provider_repo"), "icon": "bi bi-people"},
    {"label": "Productos", "href": reverse("product_repo"), "icon": "bi bi-box"},
    {"label": "Mascotas", "href": reverse("pet_repo"), "icon": "bi bi-people"},
    {"label": "Medicamentos", "href": reverse("medicine_repo"), "icon": "bi bi-people"},
    {"label": "Veterinarios", "href": reverse("veterinary_repo"), "icon": "bi bi-people"},
]


def navbar(request):
    def add_active(link):
        copy = link.copy()

        if copy["href"] == "/":
            copy["active"] = request.path == "/"
        else:
            copy["active"] = request.path.startswith(copy.get("href", ""))

        return copy

    return {"links": map(add_active, links)}