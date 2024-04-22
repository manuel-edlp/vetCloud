import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect, Browser

from django.urls import reverse

from app.models import Client

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 1) == 1


class PlaywrightTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser: Browser = playwright.firefox.launch(headless=headless)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    def test_should_have_navbar_with_links(self):
        self.page.goto(self.live_server_url)

        navbar_home_link = self.page.get_by_test_id("navbar-Home")

        expect(navbar_home_link).to_be_visible()
        expect(navbar_home_link).to_have_text("Home")
        expect(navbar_home_link).to_have_attribute("href", reverse("home"))

        navbar_clients_link = self.page.get_by_test_id("navbar-Clientes")

        expect(navbar_clients_link).to_be_visible()
        expect(navbar_clients_link).to_have_text("Clientes")
        expect(navbar_clients_link).to_have_attribute("href", reverse("clients_repo"))

    def test_should_have_home_cards_with_links(self):
        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )
        client.save()

        client = Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="221232555",
            email="goleador@gmail.com",
        )
        client.save()

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))


class ClientCreateTestCase(PlaywrightTestCase):
    def test_should_can_create_a_new_client(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono")
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido")
        ).to_be_visible()
