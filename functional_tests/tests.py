import re
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect, Browser

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


class HomeTest(PlaywrightTestCase):
    def test_should_have_navbar_with_links(self):
        page = self.browser.new_page()
        page.goto(self.live_server_url)

        navbar_home_link = page.get_by_test_id("navbar-Home")

        expect(navbar_home_link).to_be_visible()
        expect(navbar_home_link).to_have_text("Home")
        expect(navbar_home_link).to_have_attribute("href", "/")

        navbar_clients_link = page.get_by_test_id("navbar-Clientes")

        expect(navbar_clients_link).to_be_visible()
        expect(navbar_clients_link).to_have_text("Clientes")
        expect(navbar_clients_link).to_have_attribute("href", "/clientes/")

    def test_should_have_home_cards_with_links(self):
        page = self.browser.new_page()
        page.goto(self.live_server_url)

        home_clients_link = page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", "/clientes/")

class ClientsRepoTest(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/clientes/")

        expect(page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com"
        )
        client.save()

        client = Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="221232555",
            email="goleador@gmail.com"
        )
        client.save()

        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/clientes/")

        expect(page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(page.get_by_text("13 y 44")).to_be_visible()
        expect(page.get_by_text("221555232")).to_be_visible()
        expect(page.get_by_text("brujita75@hotmail.com")).to_be_visible()

        expect(page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(page.get_by_text("1 y 57")).to_be_visible()
        expect(page.get_by_text("2212322555")).to_be_visible()
        expect(page.get_by_text("goleador@gmail.com")).to_be_visible()