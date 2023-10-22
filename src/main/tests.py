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

class AboutUsTestCases(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_title(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MedVoyage | About Us")

    def test_about_nav(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        for nav_field in NavBar_Fields:
            self.assertContains(response, nav_field)

    def test_about_footer(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<p>&copy; MedVoyage</p>")

    def test_aboutus_content(self):
        content = "Looking for a hassle-free, efficient, and seamless "
        "healthcare access experience? Look no further than MedVoyage "
        "- the ultimate online appointment booking system designed to "
        "simplify and expedite the appointment process for patients "
        "and healthcare professionals. With MedVoyage, you can enjoy "
        "tailored doctor selections based on your preferences, ensuring"
        " you get the best possible care. What's more, our web-based "
        "application guarantees secure personal data protection, so "
        "you can rest easy knowing your information is safe. "
        "Revolutionize your healthcare access with MedVoyage - Sign Up "
        "today and experience unparalleled convenience and efficiency."

        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>About Us</h1>")
        self.assertContains(response, content)

    def test_about_dev_list(self):
        developers = [
            {'name': 'Kalyan Cheerla', 'bio': 'Project Manager', 'image': 'images/ProfilePic.jpg'},
            {'name': 'Bhavani Rachakatla', 'bio': 'Design and Testing Lead', 'image': 'images/ProfilePic.jpg'},
            {'name': 'Yasmeen Haleem', 'bio': 'Requirements and Documentation Lead', 'image': 'images/ProfilePic.jpg'},
            {'name': 'Demir Altay', 'bio': 'Implementation Lead(backend)', 'image': 'images/ProfilePic.jpg'},
            {'name': 'Vidhi Bhatt', 'bio': 'Implementation Lead(front end)', 'image': 'images/ProfilePic.jpg'},
            {'name': 'Emmie Abels', 'bio': 'Implementation Lead(front end)', 'image': 'images/ProfilePic.jpg'},
            {'name': 'Manushree Buyya', 'bio': 'Demo and Presentation Lead', 'image': 'images/ProfilePic.jpg'},
            {'name': 'Pravallika Bollavaram', 'bio': 'Configuration Management Lead', 'image': 'images/ProfilePic.jpg'},
        ]

        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        for developer in developers:
            self.assertContains(response, developer["name"])
            self.assertContains(response, developer["bio"])
            self.assertContains(response, developer["image"])

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
        self.assertContains(response, "<p>+123 456 7890</p>")

        # Email
        self.assertContains(response, "fa-envelope")
        self.assertContains(response, "<h4>Email</h4>")
        self.assertContains(response, "<p>contact@medvoyage.com</p>")

        # Location
        self.assertContains(response, "fa-map-marker")
        self.assertContains(response, "<h4>Location</h4>")
        self.assertContains(response, "<p>123 Street, Denton, United States</p>")

    def test_contact_message(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact Us")
        self.assertContains(response, "Name:")
        self.assertContains(response, "Email:")
        self.assertContains(response, "Message:")

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
        self.assertContains(response, '<button type="submit" class="btn btn-primary col-mt-3 mx-auto">Sign-Up</button>')

