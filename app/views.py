from django.shortcuts import get_object_or_404, redirect, render, reverse

from .models import CityEnum, Client, Medicine, Pet, Product, Provider, Veterinary

from django.db.models import Q

from django.http import JsonResponse

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from io import BytesIO


def home(request):
    """
    Renderiza la página de inicio.
    """
    return render(request, "home.html")


def clients_repository(request):
    """
    Renderiza la lista de clientes.
    """
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients})

def clients_form(request, id=None):
    """
    Renderiza el formulario de clientes y maneja la creación o actualización de clientes.
    """
    ciudades = CityEnum.choices
    if request.method == "POST":
        client_id = request.POST.get("id", "")
        errors = {}
        saved = False

        if client_id == "":
            saved, errors = Client.save_client(request.POST)
        else:
            client = get_object_or_404(Client, pk=client_id)
            update_result = client.update_client(request.POST)
            if update_result is not None:
                saved, errors = update_result
            else:
                saved = True

        if saved:
            return redirect(reverse("clients_repo"))

        return render(
            request, "clients/form.html", {"errors": errors, "client": request.POST, "ciudades": ciudades},)

    client = None
    if id is not None:
        client = get_object_or_404(Client, pk=id)

    return render(request, "clients/form.html", {"client": client, "ciudades": ciudades})


def clients_delete(request):
    """
    Elimina un cliente.
    """
    client_id = request.POST.get("client_id")
    client = get_object_or_404(Client, pk=int(client_id))
    client.delete()

    return redirect(reverse("clients_repo"))

# Proveedor
def provider_repository(request):
    """
    Renderiza la lista de proveedores.
    """
    providers = Provider.objects.all()
    return render(request, "providers/repository.html", {"providers": providers})


def provider_form(request, id=None):
    """
    Renderiza el formulario de proveedores y maneja la creación o actualización de proveedores.
    """
    if request.method == "POST":
        provider_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if provider_id == "":
            saved, errors = Provider.save_provider(request.POST)
        else:
            provider = get_object_or_404(Provider, pk=provider_id)
            saved, errors = provider.update_provider(request.POST)

        if saved:
            return redirect(reverse("provider_repo"))

        return render(
            request, "providers/form.html", {"errors": errors, "provider": request.POST},
        )

    provider = None
    if id is not None:
        provider = get_object_or_404(Provider, pk=id)

    return render(request, "providers/form.html", {"provider": provider})


def provider_delete(request):
    """
    Elimina un proveedor.
    """
    provider_id = request.POST.get("provider_id")
    provider = get_object_or_404(Provider, pk=int(provider_id))
    provider.delete()

    return redirect(reverse("provider_repo"))


# Configurar las credenciales y el cliente para Azure Computer Vision
KEY = '6cd151994fa843228f17ff671b3719e9'
ENDPOINT = 'https://vet-vision.cognitiveservices.azure.com/'
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# Producto
def product_repository(request):
    """
    Renderiza la lista de productos.
    """
    products = Product.objects.all()
    return render(request, "products/repository.html", {"products": products})

def extract_text_from_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            # Obtener la imagen del formulario
            image_file = request.FILES['image']

            # Leer los bytes de la imagen
            img_bytes = image_file.read()

            # Llamar al servicio de Computer Vision para extraer texto de la imagen
            result = computervision_client.read_in_stream(BytesIO(img_bytes), raw=True)

            # Obtener el ID de operación para hacer un seguimiento del estado
            operation_location_remote = result.headers["Operation-Location"]
            operation_id = operation_location_remote.split("/")[-1]

            # Hacer un seguimiento del estado de la operación para obtener el texto extraído
            while True:
                get_text_results = computervision_client.get_read_result(operation_id)
                if get_text_results.status not in [OperationStatusCodes.running]:
                    break

            # Procesar resultados y extraer texto
            extracted_text = ""
            for text_result in get_text_results.analyze_result.read_results:
                for line in text_result.lines:
                    extracted_text += line.text + " "

            # Devolver el texto extraído como respuesta JSON
            return JsonResponse({'extracted_text': extracted_text.strip()})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Se esperaba una imagen en la solicitud'}, status=400)

def product_form(request, id=None):
    """
    Renderiza el formulario de productos y maneja la creación o actualización de productos.
    """

    providers = Provider.objects.all()

    if request.method == "POST":
        product_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if product_id == "":
            # Obtén la imagen del formulario
            product_image = request.FILES.get("image")
            saved, errors = Product.save_product(request.POST, product_image)  # Pasa la imagen

            # Obtener el ID del proveedor seleccionado del formulario
            provider_id = request.POST.get("provider", "")

            # Asociar el proveedor seleccionado con el producto creado
            if provider_id:
                product = Product.objects.latest('id')  # Obtener el último producto creado
                product.provider_id = provider_id
                product.save()

        else:
            product = get_object_or_404(Product, pk=product_id)
            product_image = request.FILES.get("image")
            saved,errors = product.update_product(request.POST,product_image)  # Pasar request.FILES
            
            # Obtener el ID del proveedor seleccionado del formulario
            provider_id = request.POST.get("provider", "")

            # Asociar el proveedor seleccionado con el producto actualizado
            if provider_id:
                product.provider_id = provider_id
                product.save()

        if saved:
            return redirect(reverse("product_repo"))

        return render(
            request, "products/form.html", {"errors": errors, "product": request.POST, "providers": providers}
        )
    product = None
    if id is not None:
        product = get_object_or_404(Product, pk=id)

    return render(request, "products/form.html", {"product": product, "providers": providers})


def product_delete(request):
    """
    Elimina un producto.
    """
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, pk=int(product_id))
    product.delete()

    return redirect(reverse("product_repo"))

def product_search(request):
    query = request.GET.get('search')

    if query:
        # Realiza la búsqueda en varios campos utilizando Q objects
        products = Product.objects.filter(
            Q(name__icontains=query) |  # Búsqueda por nombre que contiene la consulta
            Q(description__icontains=query) |  # Búsqueda por descripción que contiene la consulta
            Q(type__icontains=query) | # Búsqueda por dosis que contiene la consulta
            Q(price__icontains=query) | # Búsqueda por precio que contiene la consulta
            Q(provider__name__icontains=query) # Búsqueda por nombre de proveedor que contiene la consulta          
        )
    else:
        products = Product.objects.all()

    context = {'products': products, 'query': query}
    return render(request, 'products/repository.html', context)

# Mascota
def pet_repository(request):
    """
    Renderiza la lista de mascotas.
    """
    pets = Pet.objects.all()
    return render(request, "pets/repository.html", {"pets": pets})

def pet_form(request, id=None):
    """
    Renderiza el formulario de mascotas y maneja la creación o actualización de mascotas.
    """
    clients = Client.objects.all()
    if request.method == "POST":
        pet_id = request.POST.get("id", "")
        errors = {}
        saved = False

        if pet_id == "":
            saved, errors = Pet.save_pet(request.POST) 
            # Si el objeto Pet se ha creado correctamente
            if saved:
                # Obtener el ID del cliente seleccionado del formulario
                client_id = request.POST.get("client", "")
                # Asociar el cliente seleccionado con el animal creado
                if client_id:
                    pet = Pet.objects.latest('id')  # Obtener el último animal creado
                    pet.client_id = client_id
                    pet.save()
        else:
            pet = get_object_or_404(Pet, pk=pet_id)
            saved, errors = pet.update_pet(request.POST)

            # Obtener el ID del cliente seleccionado del formulario
            client_id = request.POST.get("client", "")
            # Asociar el cliente seleccionado con el animal actualizado
            if client_id:
                pet.client_id = client_id
                pet.save()
                
        if saved:
            return redirect(reverse("pet_repo"))

        return render(
            request, "pets/form.html", {"errors": errors, "pet": request.POST,},
        )

    pet = None
    if id is not None:
        pet = get_object_or_404(Pet, pk=id)

    return render(request, "pets/form.html", {"pet": pet,"clients": clients})


def pet_delete(request):
    """
    Elimina una mascota.
    """
    pet_id = request.POST.get("pet_id")
    pet = get_object_or_404(Pet, pk=int(pet_id))
    pet.delete()

    return redirect(reverse("pet_repo"))

# Mascota Historial

def pet_history(request, id):
    pet = get_object_or_404(Pet.objects.prefetch_related("medicines", "veterinaries"), id=id)

    context = {
        "pet": pet,
    }
    return render(request, "pets/history.html", context)

def pet_form_history(request, id):
    veterinaries = Veterinary.objects.all()
    medicines = Medicine.objects.all()
    pet = get_object_or_404(Pet, id=id)

    if request.method == 'POST':
        pet_id = request.POST.get("id", "")
        errors = {}
        saved = True
        
        if pet_id == "":
            saved, errors = Pet.save_pet(request.POST)
            medicine_id = request.POST.get("medicines", "")
            vet_id = request.POST.get("veterinaries", "")
            
            if medicine_id and vet_id:
                pet.medicines.add(medicine_id)
                pet.veterinaries.add(vet_id)
                pet.save()
        else:
            pet = get_object_or_404(Pet, pk=pet_id)
            pet.update_pet(request.POST)
            
            medicine_id = request.POST.get("medicines", "")
            vet_id = request.POST.get("veterinaries", "")
            
            if medicine_id and vet_id:
                pet.medicines.add(medicine_id)
                pet.veterinaries.add(vet_id)
                pet.save()
        
        if saved:
            return redirect(reverse("pets_history", args=(id,)))

        # Si no se guarda correctamente, debe retornar algo
        return render(request, 'pets/history.html', {
            'pet': pet,
            'veterinaries': veterinaries,
            'medicines': medicines,
            'errors': errors,  # Muestra errores si hay
        })
    
    # Manejo para solicitudes GET
    return render(request, 'pets/form_history.html', {
        'pet': pet,
        'veterinaries': veterinaries,
        'medicines': medicines,
    })


# Veterinario

def veterinary_repository(request):
    """
    Renderiza la lista de veterinarios.
    """
    veterinaries = Veterinary.objects.all()
    return render(request, "veterinaries/repository.html", {"veterinaries": veterinaries})


def veterinary_form(request, id=None):
    """
    Renderiza el formulario de veterinarios y maneja la creación o actualización de veterinarios.
    """
    if request.method == "POST":
        veterinary_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if veterinary_id == "":
            saved, errors = Veterinary.save_veterinary(request.POST)
        else:
            veterinary = get_object_or_404(Veterinary, pk=veterinary_id)
            saved, errors =  veterinary.update_veterinary(request.POST)
          
           

        if saved:
            return redirect(reverse("veterinary_repo"))

        return render(
            request, "veterinaries/form.html", {"errors": errors, "veterinary": request.POST},
        )

    veterinary = None
    if id is not None:
        veterinary = get_object_or_404(Veterinary, pk=id)

    return render(request, "veterinaries/form.html", {"veterinary": veterinary})


def veterinary_delete(request):
    """
    Elimina un veterinario.
    """
    veterinary_id = request.POST.get("veterinary_id")
    veterinary = get_object_or_404(Veterinary, pk=int(veterinary_id))
    veterinary.delete()

    return redirect(reverse("veterinary_repo"))

# Funciones para Medicamentos
def medicine_repository(request):
    """
    Renderiza la lista de medicamentos.
    """
    medicines = Medicine.objects.all()
    return render(request, "medicines/repository.html", {"medicines": medicines})

def medicine_form(request, id=None):
    """
    Renderiza el formulario de medicamentos y maneja la creación o actualización de medicamentos.
    """
    medicine = None  # Asignar un valor predeterminado a la variable medicine
    if request.method == "POST":
        medicine_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if medicine_id == "":
            medicine_image = request.FILES.get("image")
            saved, errors = Medicine.save_medicine(request.POST,medicine_image)
        else:
            medicine = get_object_or_404(Medicine, pk=medicine_id)
            medicine_image = request.FILES.get("image")
            saved, errors = medicine.update_medicine(request.POST,medicine_image)

        if saved:
            return redirect(reverse("medicine_repo"))

        return render(
            request, "medicines/form.html", {"errors": errors, "medicine": request.POST}
        )

    medicine = None
    if id is not None:
        medicine = get_object_or_404(Medicine, pk=id)

    return render(request, "medicines/form.html", {"medicine": medicine})

def medicine_delete(request):
    """
    Elimina un medicamento.
    """
    medicine_id = request.POST.get("medicine_id")
    medicine = get_object_or_404(Medicine, pk=int(medicine_id))
    medicine.delete()

    return redirect(reverse("medicine_repo"))

def medicine_search(request):
    query = request.GET.get('search')

    if query:
        # Realiza la búsqueda en varios campos utilizando Q objects
        medicines = Medicine.objects.filter(
            Q(name__icontains=query) |  # Búsqueda por nombre que contiene la consulta
            Q(description__icontains=query) |  # Búsqueda por descripción que contiene la consulta
            Q(dose__icontains=query)  # Búsqueda por dosis que contiene la consulta
        )
    else:
        medicines = Medicine.objects.all()

    context = {'medicines': medicines, 'query': query}
    return render(request, 'medicines/repository.html', context)