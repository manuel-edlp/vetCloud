from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client,Pet,Provider,Medicine
from datetime import datetime
from django.utils import timezone 
from app.models import Product



class HomePageTest(TestCase):
    def test_use_home_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ClientsTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("clients_repo")) 
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_repo_display_all_clients(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("clients_form"))
        self.assertTemplateUsed(response, "clients/form.html")

    def test_can_create_client(self):

        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "email": "brujita75@vetsoft.com",
                "city": "La Plata",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)
        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "54221555232")
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")
        self.assertEqual(clients[0].city, "La Plata")

        self.assertRedirects(response, reverse("clients_repo"))

    def test_validation_errors_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese una ciudad")

    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "city": "La Plata",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_edit_user_with_valid_data_test(self):
        """"
        test para editar un cliente con datos validos.
        """
        client = Client.objects.create(
            name="Guido Carrillo",
            city="La Plata",
            phone="54221555232",
            email="guido@vetsoft.com",
        )

        response = self.client.post(
            reverse("clients_form"),
              data={
                "id": client.id,
                "name": "Juan Sebastian Veron",
                "phone": "221456789",
                "email": "brujita71@vetsoft.com",
                "city": "Berisso",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.name, "Juan Sebastian Veron")
        self.assertEqual(editedClient.email, "brujita71@vetsoft.com")
        self.assertEqual(editedClient.phone, "221456789")
        self.assertEqual(editedClient.city, "Berisso")

    def test_edit_user_with_invalid_data_test_city(self):

        client = Client.objects.create(
            name="Guido Carrillo",
            city="La Plata",
            phone="221456789",
            email="brujita75@vetsoft.com",
        )
    

        self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Juan Sebastian Veron",
                "phone": "221456789",
                "city": "Rosario",
                "email": "brujita75@vetsoft.com",
            },
        )

        # redirect after post
        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.city, "La Plata")

class MedicineIntegrationTest(TestCase):
    def test_can_create_medicine(self):
        response = self.client.post(
            reverse("medicine_form"),
            data={
                "name": "Paracetamol",
                "description": "Analgesic and antipyretic",
                "dose": 5,
            },
        )
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "Paracetamol")
        self.assertEqual(medicines[0].description, "Analgesic and antipyretic")
        self.assertEqual(medicines[0].dose, 5)

        self.assertRedirects(response, reverse("medicine_repo"))

    def test_validation_errors_create_medicine(self):
        response = self.client.post(
            reverse("medicine_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese una descripción")
        self.assertContains(response, "Por favor ingrese una dosis")

    def test_validation_valid_dose(self):
        response = self.client.post(
            reverse("medicine_form"),
            data={
                "name": "prueba",
                "description": "qwe",
                "dose": 4,
            },
        )
        self.assertEqual(response.status_code, 302) # verificamos medicina creada tras la redireccion

    def test_validation_invalid_dose_is_greater_than_10(self):
        response = self.client.post(
            reverse("medicine_form"),
            data={
                "name": "prueba",
                "description": "qwe",
                "dose": 13,
            },
        )
        self.assertContains(response, "La dosis debe estar en un rango de 1 a 10")
        
    def test_validation_invalid_dose_is_less_than_1(self):
        response = self.client.post(
            reverse("medicine_form"),
            data={
                "name": "prueba",
                "description": "qwe",
                "dose": -1,
            },
        )
        self.assertContains(response, "La dosis debe estar en un rango de 1 a 10")
class ProviderTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("provider_repo"))
        self.assertTemplateUsed(response, "providers/repository.html")

    def test_can_create_provider(self):
        response = self.client.post(
            reverse("provider_form"),
            data={
                "name": "Juan Roman Riquelme",
                "email": "senor10@hotmail.com",
                "address": "13 y 44",
            },
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Juan Roman Riquelme")
        self.assertEqual(providers[0].email, "senor10@hotmail.com")
        self.assertEqual(providers[0].address, "13 y 44")

        self.assertRedirects(response, reverse("provider_repo"))
    
    def test_validation_invalid_email(self): #Agrego una función ajena a la funcionalidad agregada para mayor calidad.
        response = self.client.post(
            reverse("provider_form"),
            data={
                "name": "Juan Roman Riquelme",
                "email": "senor10",
                "address": "13 y 44",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_validation_address_null(self): #Agrego una función especifica del issue
        #La modificacion es que la direccion es obligatoria. Comprueba que al poner una direccion vacia devuelva el mensaje de error
        response = self.client.post(
            reverse("provider_form"),
            data={
                "name": "Juan Roman Riquelme",
                "email": "senor10@gmail.com",
                "address": "",
            },
        )

        providers = Provider.objects.all()
        self.assertEqual(len(providers), 0)

        self.assertContains(response, "Por favor, ingrese una direccion")


class PetsTest(TestCase):
    def test_create_pet_with_valid_weight(self):
        # Crear un mascota con peso válido
        response = self.client.post(
            reverse("pet_form"), 
            data={
                "name": "Frida",
                "breed": "negrita",
                "birthday": "2017-01-01",
                "weight": "4" # Peso válido
            },
        )

        # Verificar que la mascota se haya creado correctamente
        pets = Pet.objects.all()
        self.assertEqual(len(pets), 1)

        # Verificar los detalles del mascota creado
        self.assertEqual(pets[0].name, "Frida")
        self.assertEqual(pets[0].breed, "negrita")
        self.assertEqual(pets[0].birthday, datetime(2017, 1, 1).date())
        self.assertEqual(pets[0].weight, 4)  # Peso válido

        # Verificar la redirección después de crear el mascota
        self.assertRedirects(response, reverse("pet_repo"))

    def test_create_product_with_invalid_weight(self):
        # Intentar crear una mascota con precio negativo
        response = self.client.post(
            reverse("pet_form"),
            data={
                "name": "Frida",
                "breed": "negrita",
                "birthday": "2017-01-01",
                "weight": "-10", # Peso inválido
            },
        )

        # Verificar que la mascota no se haya creado debido al peso inválido
        pets = Pet.objects.all()
        self.assertEqual(len(pets), 0)

        # Verificar que se muestra un mensaje de error en la respuesta
        self.assertContains(response, "El peso debe ser mayor a cero")
        
          
    def test_create_pet_with_valid_birthday(self):
        # Crear una mascota con fecha de nacimiento válida
        response = self.client.post(
            reverse("pet_form"), 
            data={
                "name": "Frida",
                "breed": "negrita",
                "birthday": "2013-01-01",  # Fecha de nacimiento válida
                "weight": "4",
            },
        )

        # Verificar que la mascota se haya creado correctamente
        pets = Pet.objects.all()
        self.assertEqual(len(pets), 1)

        # Verificar los detalles de la mascota creada
        self.assertEqual(pets[0].name, "Frida")
        self.assertEqual(pets[0].breed, "negrita")
        self.assertEqual(pets[0].birthday, datetime(2013, 1, 1).date())  # Convertir a objeto Date
        self.assertEqual(pets[0].weight, 4)

        # Verificar la redirección después de crear la mascota
        self.assertRedirects(response, reverse("pet_repo"))

    def test_create_pet_with_invalid_birthday(self):
        # Intentar crear una mascota con fecha de nacimiento en el futuro
        future_date = datetime.now().date() + timezone.timedelta(days=1)
        response = self.client.post(
            reverse("pet_form"),
            data={
                "name": "Frida",
                "breed": "negrita",
                "birthday": future_date.strftime("%Y-%m-%d"),  # Fecha de nacimiento en el futuro
                "weight": "4",
            },
        )

        # Verificar que la mascota no se haya creado debido a la fecha de nacimiento inválida
        pets = Pet.objects.all()
        self.assertEqual(len(pets), 0)

        # Verificar que se muestra un mensaje de error en la respuesta
        self.assertContains(response, "La fecha de nacimiento debe ser menor a la fecha actual")


class ProductsTest(TestCase):
    def test_create_product_with_valid_price(self):
        # Crear un producto con precio válido
        response = self.client.post(
            reverse("product_form"), 
            data={
                "name": "Producto Test",
                "product_type": "Tipo Test",
                "price": "10.00",  # Precio válido
            },
        )

        # Verificar que el producto se haya creado correctamente
        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        # Verificar los detalles del producto creado
        self.assertEqual(products[0].name, "Producto Test")
        self.assertEqual(products[0].product_type, "Tipo Test")
        self.assertEqual(products[0].price, 10.00)  # Precio válido

        # Verificar la redirección después de crear el producto
        self.assertRedirects(response, reverse("product_repo"))

    def test_create_product_with_invalid_price(self):
        # Intentar crear un producto con precio negativo
        response = self.client.post(
            reverse("product_form"),
            data={
                "name": "Producto Test",
                "product_type": "Tipo Test",
                "price": "-5.00",  # Precio inválido (negativo)
            },
        )

        # Verificar que el producto no se haya creado debido al precio inválido
        products = Product.objects.all()
        self.assertEqual(len(products), 0)

        # Verificar que se muestra un mensaje de error en la respuesta
        self.assertContains(response, "El precio debe ser mayor que cero")

    def test_create_product_with_non_numeric_price(self):
        # Intentar crear un producto con precio no numérico
        response = self.client.post(
            reverse("product_form"),
            data={
                "name": "Producto Test",
                "product_type": "Tipo Test",
                "price": "precio_invalido",  # Precio inválido (no numérico)
            },
        )

        # Verificar que el producto no se haya creado debido al precio inválido
        products = Product.objects.all()
        self.assertEqual(len(products), 0)

        # Verificar que se muestra un mensaje de error en la respuesta
        self.assertContains(response, "El precio debe ser un número válido")
