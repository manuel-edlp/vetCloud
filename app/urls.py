from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    path("clientes/", view=views.clients_repository, name="clients_repo"),
    path("clientes/nuevo/", view=views.clients_form, name="clients_form"),
    path("clientes/editar/<int:id>/", view=views.clients_form, name="clients_edit"),
    path("clientes/eliminar/", view=views.clients_delete, name="clients_delete"),
    path("proveedor/", view=views.provider_repository, name="provider_repo"),
    path("proveedor/nuevo/", view=views.provider_form, name="provider_form"),
    path("proveedor/editar/<int:id>/", view=views.provider_form, name="provider_edit"),
    path("proveedor/eliminar/", view=views.provider_delete, name="provider_delete"),
    # Mascota
    path("mascota/", view=views.pet_repository, name="pet_repo"),
    path("mascota/nuevo/", view=views.pet_form, name="pet_form"),
    path("mascota/editar/<int:id>/", view=views.pet_form, name="pet_edit"),
    path("mascota/eliminar/", view=views.pet_delete, name="pet_delete"),
]
