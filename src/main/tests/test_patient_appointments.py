from django.test import TestCase, Client

class PatientUpcomingAndPastAppointmentsTestCases(TestCase):
    def setUp(self):
        self.client = Client()

    def test_appt_page(self):
        response = self.client.post('/signup/', data={
            'username': 'pspk',
            'first_name': 'pk',
            'last_name': 'ps',
            'email': 'pspk@yahoo.com',
            'phone': '9999999999',
            'security_question': 'Sector 401, Underworld, Mars, Milkyway',
            'password': '#idkidk0',
            'password2': '#idkidk0',
            'login_type': 'doctor',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/login/', data={
            'username': 'pspk',
            'password': '#idkidk0',
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/client_appointments/')
        self.assertEqual(response.status_code, 200)

    def test_appt_nav(self):
        response = self.client.post('/signup/', data={
            'username': 'pspk',
            'first_name': 'pk',
            'last_name': 'ps',
            'email': 'pspk@yahoo.com',
            'phone': '9999999999',
            'security_question': 'Sector 401, Underworld, Mars, Milkyway',
            'password': '#idkidk0',
            'password2': '#idkidk0',
            'login_type': 'doctor',
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/login/', data={
            'username': 'pspk',
            'password': '#idkidk0',
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        
    def test_no_appt_listing_when_no_appt_made(self):
        response = self.client.post('/signup/', data={
            'username': 'pspk',
            'first_name': 'pk',
            'last_name': 'ps',
            'email': 'pspk@yahoo.com',
            'phone': '9999999999',
            'security_question': 'Sector 401, Underworld, Mars, Milkyway',
            'password': '#idkidk0',
            'password2': '#idkidk0',
            'login_type': 'doctor',
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/login/', data={
            'username': 'pspk',
            'password': '#idkidk0',
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/client_appointments/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Upcoming Appointments")

    def test_page_inaccessible_when_not_logged_in(self):
        response = self.client.get('/client_appointments/')
        self.assertNotEqual(response.status_code, 200)

