from django.test import TestCase, Client

NavBar_Fields = ["MedVoyage", "About", "Contact", "Login/Signup"]

class ResetPasswordTestCases(TestCase):
    def setUp(self):
        self.client = Client()

    def test_resetpassword_success(self):
        # signup login signout
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
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/doctor_dashboard/')

        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        for nav_field in NavBar_Fields + ['<a href="/signout/" class="nav-link" > Sign Out</a>']:
            self.assertContains(response, nav_field)

        response = self.client.get('/signout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')

        # reset password
        response = self.client.post('/reset_password/', data={
            'username': 'pspk',
            'new_password': 'pass1234',
            'security_question': 'Sector 401, Underworld, Mars, Milkyway',
        })
        self.assertEqual(response.status_code, 302)

        # login signout
        response = self.client.post('/login/', data={
            'username': 'pspk',
            'password': 'pass1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/doctor_dashboard/')

        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        for nav_field in NavBar_Fields + ['<a href="/signout/" class="nav-link" > Sign Out</a>']:
            self.assertContains(response, nav_field)

        response = self.client.get('/signout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')

    def test_reset_password_content(self):
        response = self.client.get('/reset_password/')
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
        self.assertContains(response, '<h2 class="card-title text-center">Reset Password</h2>')
        self.assertContains(response, '<label for="id_username">Username</label>')
        self.assertContains(response, '<input type="text" class="form-control form-control-lg" id="id_username" name="username" placeholder="JohnDoe">')
        self.assertContains(response, '<label for="id_password">New Password</label>')
        self.assertContains(response, '<input type="password" class="form-control form-control-lg" id="id_password" name="new_password" placeholder="Enter your new password">')
        self.assertContains(response, '<button type="submit" class="btn btn-primary btn-block text-center btn-mv-green">Reset</button>')
        # links
        self.assertContains(response, '<a class="text-mv-green" href="/signup/">Don\'t have an account? Sign Up Here</a>')
        self.assertNotContains(response, '<a class="text-mv-green" href="/reset_password/">Forgot Password? Reset Here</a>')

    def test_resetpassword_wrong_secquestion(self):
        # signup login signout
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

        # reset password
        response = self.client.post('/reset_password/', data={
            'username': 'pspk',
            'new_password': 'pass1234',
            'security_question': 'Sector 404, Underworld, Mars, Milkyway',
        })
        self.assertEqual(response.status_code, 200)

        # login signout
        response = self.client.post('/login/', data={
            'username': 'pspk',
            'password': 'pass1234',
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        for nav_field in NavBar_Fields:
            self.assertContains(response, nav_field)

    def test_resetpassword_wrong_userid(self):
        # signup login signout
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

        # reset password
#        response = self.client.post('/reset_password/', data={
#            'username': 'pkps',
#            'new_password': 'pass1234',
#            'security_question': 'Sector 401, Underworld, Mars, Milkyway',
#        })
#        self.assertEqual(response.status_code, 200)

        # login signout
        response = self.client.post('/login/', data={
            'username': 'pkps',
            'password': 'pass1234',
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        for nav_field in NavBar_Fields:
            self.assertContains(response, nav_field)

    def test_resetpassword_short_success(self):
        # signup login signout
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
        self.assertEqual(response.url, '/')

        # reset password
        response = self.client.post('/reset_password/', data={
            'username': 'pspk',
            'new_password': 'pass1234',
            'security_question': 'Sector 401, Underworld, Mars, Milkyway',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')

        # login signout
        response = self.client.post('/login/', data={
            'username': 'pspk',
            'password': 'pass1234',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        for nav_field in NavBar_Fields + ['<a href="/signout/" class="nav-link" > Sign Out</a>']:
            self.assertContains(response, nav_field)
