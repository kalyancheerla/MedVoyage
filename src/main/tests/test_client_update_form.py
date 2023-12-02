from django.test import TestCase, Client
from main.models import User

ClientNavBar_Fields = ["MedVoyage", "About", "Contact", "Profile","Sign Out"]

class ClientUpdateFormTestCases(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='johndoe', password='password123')
        self.client = Client()
        self.client.login(username='johndoe', password='password123')

    def test_update_user_info_page_is_rendered(self):

        response = self.client.get('/client_update/')
        self.assertEqual(response.status_code, 200)
        #navbar
        for nav_field in ClientNavBar_Fields:
            self.assertContains(response, nav_field)
        #footer
        self.assertContains(response, "&copy; MedVoyage")
        #content
        self.assertContains(response, '<h2 class="text-center">Update User Information</h2>')

    def test_update_user_info_form_submission(self):
        # Prepare data for form submission
        form_data = {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'phone': '1234567890',
            'email': 'newemail@example.com',
        }

        # Submit the form
        response = self.client.post('/client_update/', form_data)

        # Check if the form submission is successful and redirects to the expected page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/client_profile/')

        # Check if the user's information is updated in the database
        updated_user = User.objects.get(username='johndoe')
        self.assertEqual(updated_user.first_name, 'NewFirstName')
        self.assertEqual(updated_user.last_name, 'NewLastName')
        self.assertEqual(updated_user.phone, '1234567890')
        self.assertEqual(updated_user.email, 'newemail@example.com')


