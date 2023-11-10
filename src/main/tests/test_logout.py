from django.test import TestCase, Client

NavBar_Fields = ["MedVoyage", "About", "Contact", "Login/Signup"]

# Create your tests here.
class LogoutTestCases(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logout_success(self):
        response = self.client.post('/signup/', data={
            'username': 'pspk',
            'first_name': 'pk',
            'last_name': 'ps',
            'email': 'pspk@yahoo.com',
            'phone': '9999999999',
            'security_question': 'Sector 401, Underworld, Mars, Milkyway',
            'password': 'idk',
            'password2': 'idk',
            'login_type': 'doctor',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/login/', data={
            'username': 'pspk',
            'password': 'idk',
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/client_dashboard/')
        self.assertEqual(response.status_code, 200)
        # nav fields
        for nav_field in NavBar_Fields + ['<a href="/signout" class="nav-link" > Sign Out</a>']:
            self.assertContains(response, nav_field)

        response = self.client.get('/signout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')

    def test_logout_notpresent(self):
        response = self.client.post('/signup/', data={
            'username': 'pspk',
            'first_name': 'pk',
            'last_name': 'ps',
            'email': 'pspk@yahoo.com',
            'phone': '9999999999',
            'security_question': 'Sector 401, Underworld, Mars, Milkyway',
            'password': 'idk',
            'password2': 'idk',
            'login_type': 'doctor',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/login/', data={
            'username': 'pspk',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        # nav field
        for nav_field in NavBar_Fields:
            self.assertContains(response, nav_field)

        self.assertNotContains(response, '<a href="/signout" class="nav-link" > Sign Out</a>')

    def test_logout_present_in_about_contact_pages(self):
        response = self.client.post('/signup/', data={
            'username': 'pspk',
            'first_name': 'pk',
            'last_name': 'ps',
            'email': 'pspk@yahoo.com',
            'phone': '9999999999',
            'security_question': 'Sector 401, Underworld, Mars, Milkyway',
            'password': 'idk',
            'password2': 'idk',
            'login_type': 'doctor',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/login/', data={
            'username': 'pspk',
            'password': 'idk',
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        for nav_field in NavBar_Fields + ['<a href="/signout" class="nav-link" > Sign Out</a>']:
            self.assertContains(response, nav_field)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        for nav_field in NavBar_Fields + ['<a href="/signout" class="nav-link" > Sign Out</a>']:
            self.assertContains(response, nav_field)

        response = self.client.get('/signout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')
