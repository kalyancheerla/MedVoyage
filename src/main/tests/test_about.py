from django.test import TestCase, Client

NavBar_Fields = ["MedVoyage", "About", "Contact", "Login/Signup"]

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

