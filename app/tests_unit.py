from django.test import TestCase
from django.utils import timezone

from app.models import Client, Medicine, Pet, Product, Provider, validate_pet


class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        """
        Prueba la creación y recuperación de un cliente.
        Esta función verifica que el sistema permita la creación de un cliente y que se pueda recuperar correctamente desde la base de datos.
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },

        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")

    def test_can_update_client(self):
        """
        Prueba la actualización de un cliente.
        Esta función testea si se puede actualizar el cliente.
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client(
                {"name": "Juan Sebastian Veron",
                "phone": "221555233",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555233")

    def test_update_client_with_error(self):
        """
        Prueba la actualización de un cliente con un error.
        Esta función testea que el sistema maneje adecuadamente los errores al intentar actualizar un cliente.
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555232")

    def test_update_client_with_email_null(self): #nuevo test verificando que no pueda hacer update con email nulo
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"email": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.email, "brujita75@vetsoft.com")
class MedicineModelTest(TestCase):
    
    def test_can_create_medicine_with_valid_dose(self):
        """
        Prueba la creación de un medicamento con una dosis válida.
        Esta función testea que el sistema permita la creación de un medicamento con una dosis válida.
        """
        success, errors = Medicine.save_medicine(
            {
                "name": "Ibuprofeno",
                "description": "Medicamento antiinflamatorio",
                "dose": 1,
            },
        )
        self.assertTrue(success)

        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)

    def test_cannot_create_medicine_with_invalid_dose(self):
        """
        Prueba la creación de un medicamento con una dosis inválida.
        Esta función verifica que el sistema no permita la creación de un medicamento con una dosis inválida.
        """
        success, errors = Medicine.save_medicine(
            {
                "name": "Ibuprofeno",
                "description": "Medicamento antiinflamatorio",
                "dose": 11,
            },
        )
        self.assertFalse(success)
        self.assertIn("dose", errors)

        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 0)

    def test_update_medicine_with_invalid_dose(self):
        """
        Prueba la actualización de un medicamento con una dosis inválida.       
        Esta función verifica que el sistema maneje adecuadamente los intentos de actualización de un medicamento con una dosis inválida.
        """
        Medicine.save_medicine(
            {
                "name": "Paracetamol",
                "description": "Medicamento para el dolor",
                "dose": 5,
            },
        )
        medicine = Medicine.objects.get(pk=1)

        self.assertEqual(medicine.dose, 5)

        success, errors = medicine.update_medicine({"dose": 11})

        self.assertFalse(success)
        self.assertIn("dose", errors)
        medicine_updated = Medicine.objects.get(pk=1)

        self.assertEqual(medicine_updated.dose, 5)

class  ProviderModelTest(TestCase):
    def test_can_create_and_get_provider(self):
        """
        Prueba la creación y recuperación de un proveedor.
        Esta función asegura de que se pueda crear un proveedor con datos válidos y luego recuperarlo correctamente de la base de datos.
        """
        Provider.save_provider(
            {
                "name": "Juan Roman Riquelme",
                "email": "senor10@gmail.com",
                "address": "13 y 44",
            },
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Juan Roman Riquelme")
        self.assertEqual(providers[0].address, "13 y 44")
        self.assertEqual(providers[0].email, "senor10@gmail.com")

    #Agrego test unitario especifico de la issue de provider
    def test_provider_address(self):
        """
        Prueba la recuperación de un proveedor por dirección específica.
        Esta función verifica que el sistema maneje correctamente tanto los proveedores con dirección como los que no tienen dirección.
        Garantizando que los datos se almacenen y recuperen correctamente de la base de datos.
        """
        addres = "calle 13 y 44"
        Provider.save_provider(
            {
                "name": "Juan Roman Riquelme",
                "email": "senor10@gmail.com",
                "address": addres, #guardo proveedor con direccion especifica
            },
        )
        provider = Provider.objects.get(address=addres) #recupero proveedor segun la direccion (supongo que no van a haber dos proveedores con esa direccion)
        self.assertEqual(provider.address, addres) #verifica que la direccion recuperada coincida con la especifica

class PetModelTest(TestCase):
    def test_validate_pet_birthday(self):
        """
        Prueba la validación de la fecha de nacimiento de una mascota.
        """
        # Probamos la validación de fecha de nacimiento para una mascota
        """
        Esta función testea la validación de fecha de nacimiento para una mascota.
        """
        valid_data = {
            "name": "Frida",
            "breed": "negrita",
            "birthday": "2013-01-01",  # Fecha de nacimiento válida
            "weight": "22",
        }
        self.assertEqual(validate_pet(valid_data), {})  # La validación debería pasar sin errores
        future_date = timezone.now().date() + timezone.timedelta(days=1)
        invalid_data = {
            "name": "Frida",
            "breed": "negrita",
            "birthday": future_date.strftime("%Y-%m-%d"),  # Fecha de nacimiento en el futuro
            "weight": "22",
        }
        expected_error = {"birthday": "La fecha de nacimiento debe ser menor a la fecha actual"}
        self.assertEqual(validate_pet(invalid_data), expected_error)  # La validación debería dar error



    # Validacion de peso mascota

    def test_create_pet_with_valid_weight(self):
        """
        Prueba la creación de una mascota con un peso válido.
        Esta función valida la creación de una mascota con peso valido.
        """
        success, message_or_errors = Pet.save_pet({
            "name": "Frida",
            "breed": "negrita",
            "birthday": "2017-01-01",
            "weight": "4", # Peso válido
        })

        self.assertTrue(success)
        self.assertEqual(message_or_errors, None)

    def test_create_pet_with_invalid_weight_negative(self):
        """
        Prueba la creación de una mascota con un peso negativo.
        Esta función verifica el comportamiento del sistema al intentar crear una mascota con un peso negativo.
        """
        success, message_or_errors = Pet.save_pet({
            "name": "Frida",
            "breed": "negrita",
            "birthday": "2017-01-01",
            "weight": "-1", # Peso inválido
        })

        self.assertFalse(success)
        self.assertIn("weight", message_or_errors)
        self.assertEqual(message_or_errors["weight"], "El peso debe ser mayor a cero")

class ProductModelTest(TestCase):
    def test_create_product_with_valid_price(self):
        """
        Prueba la creación de un producto con un precio válido.
        Esta función verifica que el sistema permita la creación de un producto con un precio válido.
        """
        success, message_or_errors = Product.save_product({
            "name": "Test Product",
            "product_type": "Test Type",
            "price": "100",
        })

        self.assertTrue(success)
        self.assertEqual(message_or_errors, "Producto creado exitosamente")

    def test_create_product_with_invalid_price_zero(self):
        """
        Prueba la creación de un producto con un precio de cero.
        Esta función verifica cómo el sistema maneja la creación de un producto con un precio igual a cero.
        """
        success, message_or_errors = Product.save_product({
            "name": "Test Product",
            "product_type": "Test Type",
           "price": "0",
         })

        self.assertFalse(success)
        self.assertIn("price", message_or_errors)
        self.assertEqual(message_or_errors["price"], "El precio debe ser mayor que cero")

    def test_create_product_with_invalid_price_negative(self):
        """
        Prueba la creación de un producto con un precio negativo.
        Esta función verifica cómo el sistema maneja la creación de un producto con un precio negativo.
        """
        success, message_or_errors = Product.save_product({
            "name": "Test Product",
          "product_type": "Test Type",
           "price": "-10",
        })

        self.assertFalse(success)
        self.assertIn("price", message_or_errors)
        self.assertEqual(message_or_errors["price"], "El precio debe ser mayor que cero")

