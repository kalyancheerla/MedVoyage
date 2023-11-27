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

    def test_footer(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "&copy; MedVoyage")

    def test_content_display(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MedVoyage')
        self.assertContains(response, 'Your journey to health begins here: Navigating Wellness with MedVoyage.')
