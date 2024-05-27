from django.test import TestCase
from app.models import Client,Pet


class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": "221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555232")

class ProductModelTest(TestCase):
    def test_create_pet_with_valid_weight(self):
        success, message_or_errors = Pet.save_pet({
            "name": "Frida",
            "breed": "negrita",
            "birthday": "2017-01-01",
            "weight": "4" # Peso válido
        })

        self.assertTrue(success)
        self.assertEqual(message_or_errors, None)

    def test_create_pet_with_invalid_weight_negative(self):
        success, message_or_errors = Pet.save_pet({
            "name": "Frida",
            "breed": "negrita",
            "birthday": "2017-01-01",
            "weight": "-1" # Peso inválido
        })

        self.assertFalse(success)
        self.assertIn("weight", message_or_errors)
        self.assertEqual(message_or_errors["weight"], "Por favor ingrese un peso correcto (debe ser mayor a cero)")
