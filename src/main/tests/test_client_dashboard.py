from django.test import TestCase, Client

ClientNavBar_Fields = ["MedVoyage", "About", "Contact", "Profile", "Sign Out"]

class ContactUsTestCases(TestCase):
    def setUp(self):
        self.client = Client()

    def test_client_dashboard_content(self):
        response = self.client.post('/signup/', data={
            'username': 'JohnDoe',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'John@email.com',
            'phone': '555-555-5555',
            'security_question': 'Dreamland',
            'password': 'password123',
            'password2': 'password123',
            'login_type': 'patient',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/login/', data={
            'username': 'JohnDoe',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/client_dashboard/')

        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        #navbar
        for nav_field in ClientNavBar_Fields:
            self.assertContains(response, nav_field)
        #footer
        self.assertContains(response, "&copy; MedVoyage")
        #content
        self.assertContains(response, f'Welcome to your Dashboard, {response.context["user"].first_name} {response.context["user"].last_name}!')

