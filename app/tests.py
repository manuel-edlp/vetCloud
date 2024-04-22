from django.test import TestCase

class HomePageTest(TestCase):
    def test_use_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed("home.html")

class ClientsTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get("/clientes/")
        self.assertTemplateUsed("clients/repository.html")
