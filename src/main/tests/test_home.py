from django.test import TestCase, Client

NavBar_Fields = ["MedVoyage", "About", "Contact", "Login/Signup"]

# Create your tests here.
class HomeViewTestCases(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_title(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MedVoyage | Home")

    def test_home_nav(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        for nav_field in NavBar_Fields:
            self.assertContains(response, nav_field)

