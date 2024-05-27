from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client,Pet


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
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

        self.assertRedirects(response, reverse("clients_repo"))

    def test_validation_errors_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")

    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_edit_user_with_valid_data(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        response = self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Guido Carrillo",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.name, "Guido Carrillo")
        self.assertEqual(editedClient.phone, client.phone)
        self.assertEqual(editedClient.address, client.address)
        self.assertEqual(editedClient.email, client.email)


class PetsTest(TestCase):
    def test_create_pet_with_valid_price(self):
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
        self.assertEqual(pets[0].birthday, "2017-01-01")
        self.assertEqual(pets[0].weight, 4)  # Precio válido

        # Verificar la redirección después de crear el mascota
        self.assertRedirects(response, reverse("pet_repo"))

    def test_create_product_with_invalid_price(self):
        # Intentar crear una mascota con precio negativo
        response = self.client.post(
            reverse("pet_form"),
            data={
                "name": "Frida",
                "breed": "negrita",
                "birthday": "2017-01-01",
                "weight": "-10" # Peso inválido
            },
        )

        # Verificar que la mascota no se haya creado debido al peso inválido
        pets = Pet.objects.all()
        self.assertEqual(len(pets), 0)

        # Verificar que se muestra un mensaje de error en la respuesta
        self.assertContains(response, "Por favor ingrese un peso correcto (debe ser mayor a cero)")
