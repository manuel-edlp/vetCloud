from django.test import TestCase
from app.models import Client,Pet,validate_pet
from django.utils import timezone


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

class PetModelTest(TestCase):
    def test_validate_pet_birthday(self):
        # Probamos la validación de fecha de nacimiento para una mascota
        valid_data = {
            "name": "Frida",
            "breed": "negrita",
            "birthday": "2013-01-01"  # Fecha de nacimiento válida
        }
        self.assertEqual(validate_pet(valid_data), {})  # La validación debería pasar sin errores
        future_date = timezone.now().date() + timezone.timedelta(days=1)
        invalid_data = {
            "name": "Frida",
            "breed": "negrita",
            "birthday": future_date.strftime("%Y-%m-%d")  # Fecha de nacimiento en el futuro
        }
        expected_error = {"birthday": "La fecha de nacimiento debe ser menor a la fecha actual"}
        self.assertEqual(validate_pet(invalid_data), expected_error)  # La validación debería dar error