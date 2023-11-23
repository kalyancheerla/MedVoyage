from django.test import TestCase, Client

NavBar_Fields = ["MedVoyage", "About", "Contact", "Login/Signup"]

class ContactUsTestCases(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_title(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MedVoyage | Contact Us")

    def test_contact_nav(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        for nav_field in NavBar_Fields:
            self.assertContains(response, nav_field)

    def test_contact_footer(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<p>&copy; MedVoyage</p>")

    def test_contact_details(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact Us")

        # Phone
        self.assertContains(response, "fa-phone")
        self.assertContains(response, "<h4>Phone</h4>")
        self.assertContains(response, "<p>(+1) 214-89-22196</p>")

        # Email
        self.assertContains(response, "fa-envelope")
        self.assertContains(response, "<h4>Email</h4>")
        self.assertContains(response, "<p>medvoyage.service@gmail.com</p>")

        # Location
        self.assertContains(response, "fa-map-marker")
        self.assertContains(response, "<h4>Location</h4>")
        self.assertContains(response, "<p>Discovery Park, N Elm Street, Denton, TX, US.</p>")

    def test_contact_message(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact Us")
        self.assertContains(response, "Name:")
        self.assertContains(response, "Email:")
        self.assertContains(response, "Message:")

