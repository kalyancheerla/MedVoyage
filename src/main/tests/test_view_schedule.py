from django.test import TestCase, Client
import datetime

NavBar_Fields = ["MedVoyage", "About", "Contact", "Profile", "Sign Out", "Help"]

class ViewScheduleTestCases(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_schedule_content(self):
        response = self.client.post('/signup/', data={
            'username': 'Do',
            'first_name': 'Do',
            'last_name': 'H',
            'email': 'Do@email.com',
            'phone': '555-555-5555',
            'security_question': 'Dreamland',
            'password': 'password123',
            'password2': 'password123',
            'login_type': 'doctor',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/login/', data={
            'username': 'Do',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/doctor_dashboard/')

        response = self.client.get('/view_schedule/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "MedVoyage | View Schedule")
        self.assertEqual(response.status_code, 200)

        for nav_field in NavBar_Fields:
            self.assertContains(response, nav_field)
        
        self.assertContains(response, "<p>&copy; MedVoyage</p>")

        self.assertContains(response, '<h3>Select the date you\'d like to see appointments for:</h3>')
        self.assertContains(response, 'input type="submit" value="View"')

    def test_view_success(self):
        response = self.client.post('/signup/', data={
            'username': 'Do',
            'first_name': 'Do',
            'last_name': 'H',
            'email': 'Do@email.com',
            'phone': '555-555-5555',
            'security_question': 'Dreamland',
            'password': 'password123',
            'password2': 'password123',
            'login_type': 'doctor',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/login/', data={
            'username': 'Do',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/doctor_dashboard/')

        response = self.client.post('/add_slots/', data={
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-0-date': '2023-11-13',
            'form-0-start_time': '09:00',
            'form-0-end_time': '10:00',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/slots/')

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

        response = self.client.post('/book-appointment/', data={
            'appointment_date': '2023-11-13',
            'doctor': 1,
            'time_slot': '09:00:00 - 10:00:00',
            'details': 'fever, cold',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/view_schedule/', data={
            'date': '2023-11-13',
        })
        self.assertEqual(response.status_code, 200)