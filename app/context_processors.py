from django.urls import reverse

# Lista de enlaces de navegación con etiquetas, hrefs e íconos
links = [
    {"label": "Inicio", "href": reverse("home"), "icon": "bi bi-house-door"},
    {"label": "Clientes", "href": reverse("clients_repo"), "icon": "bi bi-people"},
    {"label": "Proveedores", "href": reverse("provider_repo"), "icon": "bi bi-briefcase"},
    {"label": "Productos", "href": reverse("product_repo"), "icon": "bi bi-box-seam"},
    {"label": "Mascotas", "href": reverse("pet_repo"), "icon": "bi bi-piggy-bank"},
    {"label": "Medicamentos", "href": reverse("medicine_repo"), "icon": "bi bi-capsule"},
    {"label": "Veterinarios", "href": reverse("veterinary_repo"), "icon": "bi bi-person-hearts"},
]

def navbar(request):
    """
    Genera el contexto del navegador con enlaces activos basados en la URL actual.

    Args:
        request (HttpRequest): La solicitud HTTP actual.

    Returns:
        dict: Un diccionario con los enlaces de navegación, marcando el enlace activo.
    """
    def add_active(link):
        """
        Añade la clave 'active' a un enlace si la URL coincide con la ruta actual.

        Args:
            link (dict): Un diccionario que representa un enlace de navegación.

        Returns:
            dict: Una copia del enlace con la clave 'active' añadida.
        """
        copy = link.copy()

        if copy["href"] == "/":
            copy["active"] = request.path == "/"
        else:
            copy["active"] = request.path.startswith(copy.get("href", ""))

        return copy

    return {"links": map(add_active, links)}
