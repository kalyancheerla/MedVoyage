from django.test import TestCase, Client

NavBar_Fields = ["MedVoyage", "About", "Contact", "Login/Signup"]

# Create your tests here.
class LoginTestCases(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_content(self):
        response = self.client.get('/login/')
        # response code
        self.assertEqual(response.status_code, 200)
        # title
        self.assertContains(response, "MedVoyage | Login")
        # nav fields
        for nav_field in NavBar_Fields:
            self.assertContains(response, nav_field)
        # footer
        self.assertContains(response, "<p>&copy; MedVoyage</p>")

        #content
        self.assertContains(response, '<h2 class="card-title text-center">Login</h2>')
        self.assertContains(response, '<label for="id_username">Username</label>')
        self.assertContains(response, '<input type="text" class="form-control form-control-lg mb-2" id="id_username" name="username" placeholder="JohnDoe">')
        self.assertContains(response, '<label for="id_password">Password</label>')
        self.assertContains(response, '<input type="password" class="form-control form-control-lg" id="id_password" name="password" placeholder="Enter your password">')
        self.assertContains(response, '<button type="submit" class="btn btn-primary btn-block text-center mt-2">Login</button>')
        # links
        self.assertContains(response, '<a href="/signup/">Don\'t have an account? Sign Up Here</a>')
        self.assertContains(response, '<a href="/reset_password/">Forgot Password? Reset Here</a>')

    def test_login_success(self):
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
        self.assertEqual(response.url, '/home/')

        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        # nav fields
        for nav_field in NavBar_Fields + ['Sign Out']:
            self.assertContains(response, nav_field)

    def test_login_failure(self):
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

        # wrong password
        response = self.client.post('/login/', data={
            'username': 'JohnDoe',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 200)
        # title
        self.assertContains(response, "MedVoyage | Login")
        # nav fields
        for nav_field in NavBar_Fields:
            self.assertContains(response, nav_field)
        # footer
        self.assertContains(response, "<p>&copy; MedVoyage</p>")

        #content
        self.assertContains(response, '<h2 class="card-title text-center">Login</h2>')
        self.assertContains(response, '<label for="id_username">Username</label>')
        self.assertContains(response, '<input type="text" class="form-control form-control-lg mb-2" id="id_username" name="username" placeholder="JohnDoe">')
        self.assertContains(response, '<label for="id_password">Password</label>')
        self.assertContains(response, '<input type="password" class="form-control form-control-lg" id="id_password" name="password" placeholder="Enter your password">')
        self.assertContains(response, '<button type="submit" class="btn btn-primary btn-block text-center mt-2">Login</button>')
        # links
        self.assertContains(response, '<a href="/signup/">Don\'t have an account? Sign Up Here</a>')
        self.assertContains(response, '<a href="/reset_password/">Forgot Password? Reset Here</a>')

    def test_login_without_signup(self):
        response = self.client.post('/login/', data={
            'username': 'JohnDoe',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 200)
        # title
        self.assertContains(response, "MedVoyage | Login")
        # nav fields
        for nav_field in NavBar_Fields:
            self.assertContains(response, nav_field)
        # footer
        self.assertContains(response, "<p>&copy; MedVoyage</p>")

        #content
        self.assertContains(response, '<h2 class="card-title text-center">Login</h2>')
        self.assertContains(response, '<label for="id_username">Username</label>')
        self.assertContains(response, '<input type="text" class="form-control form-control-lg mb-2" id="id_username" name="username" placeholder="JohnDoe">')
        self.assertContains(response, '<label for="id_password">Password</label>')
        self.assertContains(response, '<input type="password" class="form-control form-control-lg" id="id_password" name="password" placeholder="Enter your password">')
        self.assertContains(response, '<button type="submit" class="btn btn-primary btn-block text-center mt-2">Login</button>')
        # links
        self.assertContains(response, '<a href="/signup/">Don\'t have an account? Sign Up Here</a>')
        self.assertContains(response, '<a href="/reset_password/">Forgot Password? Reset Here</a>')

