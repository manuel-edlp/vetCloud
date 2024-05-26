from django.test import TestCase
from app.models import Client, Medicine


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

class MedicineModelTest(TestCase):
    def test_can_create_and_get_medicine(self):
        success, _ = Medicine.save_medicine(
            {
                "name": "Paracetamol",
                "description": "Medicamento para el dolor",
                "dose": 5,
            }
        )
        self.assertTrue(success)

        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "Paracetamol")
        self.assertEqual(medicines[0].description, "Medicamento para el dolor")
        self.assertEqual(medicines[0].dose, 5)

    def test_cannot_create_medicine_with_invalid_dose(self):
        success, errors = Medicine.save_medicine(
            {
                "name": "Ibuprofeno",
                "description": "Medicamento antiinflamatorio",
                "dose": 11,
            }
        )
        self.assertFalse(success)
        self.assertIn("dose", errors)

        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 0)

    def test_can_update_medicine(self):
        Medicine.save_medicine(
            {
                "name": "Paracetamol",
                "description": "Medicamento para el dolor",
                "dose": 5,
            }
        )
        medicine = Medicine.objects.get(pk=1)

        self.assertEqual(medicine.dose, 5)

        success, _ = medicine.update_medicine({"dose": 7})

        self.assertTrue(success)
        medicine_updated = Medicine.objects.get(pk=1)

        self.assertEqual(medicine_updated.dose, 7)

    def test_update_medicine_with_invalid_dose(self):
        Medicine.save_medicine(
            {
                "name": "Paracetamol",
                "description": "Medicamento para el dolor",
                "dose": 5,
            }
        )
        medicine = Medicine.objects.get(pk=1)

        self.assertEqual(medicine.dose, 5)

        success, errors = medicine.update_medicine({"dose": 11})

        self.assertFalse(success)
        self.assertIn("dose", errors)
        medicine_updated = Medicine.objects.get(pk=1)

        self.assertEqual(medicine_updated.dose, 5)