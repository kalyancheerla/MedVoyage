from django.test import TestCase, Client

class SignupTemplateTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_form_rendered_correctly(self):
        response = self.client.get('/signup/')  # Adjust the URL as per your project
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

        # Check for form elements
        self.assertContains(response, '<form method="post">')
        self.assertContains(response, '<input type="hidden" name="csrfmiddlewaretoken"')
        self.assertContains(response, 'id_username')
        self.assertContains(response, 'id_first_name')
        self.assertContains(response, 'id_last_name')
        self.assertContains(response, 'id_email')
        self.assertContains(response, 'id_phone')
        self.assertContains(response, 'id_password')
        self.assertContains(response, 'id_password2')
        self.assertContains(response, '<input type="radio" name="login_type" value="patient" required id="id_login_type_0">')
        self.assertContains(response, '<input type="radio" name="login_type" value="doctor" required id="id_login_type_1">')
        self.assertContains(response, '<input type="radio" name="login_type" value="staff" required id="id_login_type_2">')
        self.assertContains(response, 'type="submit"')

    def test_form_labels_and_placeholders(self):
        response = self.client.get('/signup/')  # Adjust the URL as per your project
        self.assertEqual(response.status_code, 200)

        # Check labels and placeholders
        self.assertContains(response, 'for="id_username">Username:</label>')
        self.assertContains(response, 'placeholder="JohnDoe"')
        self.assertContains(response, 'for="id_first_name">First Name:</label>')
        self.assertContains(response, 'placeholder="John"')
        self.assertContains(response, 'for="id_last_name">Last Name:</label>')
        self.assertContains(response, 'placeholder="Doe"')
        self.assertContains(response, 'for="id_email">Email:</label>')
        self.assertContains(response, 'placeholder="John@email.com"')
        self.assertContains(response, 'for="id_phone">Phone:</label>')
        self.assertContains(response, 'placeholder="555-555-5555"')
        self.assertContains(response, 'for="id_password">Password:</label>')
        self.assertContains(response, 'placeholder="Enter password"')
        self.assertContains(response, 'for="id_password2">Confirm Password:</label>')
        self.assertContains(response, 'placeholder="Confirm password"')

    def test_form_errors_displayed(self):
        # Simulate form submission with errors
        response = self.client.post('/signup/', data={
            'username': '',  # Invalid input to trigger errors
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid_email',
            'phone': '555-555-5555',
            'password': 'password123',
            'password2': 'password456',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="alert alert-danger">')
        self.assertContains(response, "This field is required.")

    def test_form_valid_submission(self):
        # Simulate a valid form submission
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

        # Expect a redirect (status code 302) after a successful signup
        self.assertEqual(response.status_code, 302)


    def test_login_type_field_rendered(self):
        response = self.client.get('/signup/')  # Adjust the URL as per your project
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input type="radio" name="login_type" value="patient" required id="id_login_type_0">')
        self.assertContains(response, '<input type="radio" name="login_type" value="doctor" required id="id_login_type_1">')
        self.assertContains(response, '<input type="radio" name="login_type" value="staff" required id="id_login_type_2">')

    def test_submit_button_rendered(self):
        response = self.client.get('/signup/')  # Adjust the URL as per your project
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<button type="submit" class="btn btn-primary col-mt-3 mx-auto btn-mv-green">Sign-Up</button>')

