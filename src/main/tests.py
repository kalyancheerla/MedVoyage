from django.test import TestCase, Client

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
        self.assertContains(response, "MedVoyage")
        self.assertContains(response, "About")
        self.assertContains(response, "Contact")
        self.assertContains(response, "Login/Signup")
