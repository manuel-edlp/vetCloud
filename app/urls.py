from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    
    # Cliente
    path("clientes/", view=views.clients_repository, name="clients_repo"),
    path("clientes/nuevo/", view=views.clients_form, name="clients_form"),
    path("clientes/editar/<int:id>/", view=views.clients_form, name="clients_edit"),
    path("clientes/eliminar/", view=views.clients_delete, name="clients_delete"),
    
    # Proveedor
    path("proveedor/", view=views.provider_repository, name="provider_repo"),
    path("proveedor/nuevo/", view=views.provider_form, name="provider_form"),
    path("proveedor/editar/<int:id>/", view=views.provider_form, name="provider_edit"),
    path("proveedor/eliminar/", view=views.provider_delete, name="provider_delete"),
    path('proveedor/buscar/', view=views.provider_search, name='provider_search'),

    # Producto
    path("producto/", view=views.product_repository, name="product_repo"),
    path("producto/nuevo/", view=views.product_form, name="product_form"),
    path('extract_text_from_image/', views.extract_text_from_image, name='extract_text_from_image'),
    path("producto/editar/<int:id>/", view=views.product_form, name="product_edit"),
    path("producto/eliminar/", view=views.product_delete, name="product_delete"),
    path('producto/buscar/', view=views.product_search, name='product_search'),

    # Mascota
    path("mascota/", view=views.pet_repository, name="pet_repo"),
    path("mascota/nuevo/", view=views.pet_form, name="pet_form"),
    path("mascota/editar/<int:id>/", view=views.pet_form, name="pet_edit"),
    path("mascota/eliminar/", view=views.pet_delete, name="pet_delete"),  

    # Mascota Historial
    path("mascota/historial/<int:id>", view=views.pet_history, name="pet_history"),
    path("mascota/historial/<int:id>/nuevo", view=views.pet_form_history, name="pet_form_history"),
    path("mascota/historial/<int:id>/editar", view=views.pet_form_history, name="pet_edit_history"),
    path("mascota/historial/<int:id>/eliminar/", view=views.pet_delete, name="pet_delete_history"), 

    #Veterinario
    path("veterinario/", view=views.veterinary_repository, name="veterinary_repo"),
    path("veterinario/nuevo/", view=views.veterinary_form, name="veterinary_form"),
    path("veterinario/editar/<int:id>/", view=views.veterinary_form, name="veterinary_edit"),
    path("veterinario/eliminar/", view=views.veterinary_delete, name="veterinary_delete"),

     # Medicamento
    path("medicamento/", view=views.medicine_repository, name="medicine_repo"),
    path("medicamento/nuevo/", view=views.medicine_form, name="medicine_form"),
    path("medicamento/editar/<int:id>/", view=views.medicine_form, name="medicine_edit"),
    path("medicamento/eliminar/", view=views.medicine_delete, name="medicine_delete"),
    path('medicamento/buscar/', view=views.medicine_search, name='medicine_search'),
]
