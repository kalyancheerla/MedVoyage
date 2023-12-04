from django.test import TestCase, Client

NavBar_Fields = ["MedVoyage", "About", "Contact", "Login/Signup"]

class CancelAppointmentTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cancel_page_content(self):
        response = self.client.get('/cancel_appointment/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "MedVoyage | Cancel Appointment")
        self.assertEqual(response.status_code, 200)

        for nav_field in NavBar_Fields:
            self.assertContains(response, nav_field)
        
        self.assertContains(response, "<p>&copy; MedVoyage</p>")

        self.assertContains(response, '<h2>Cancel an Appointment</h2>')
        self.assertContains(response, '<label for="id_appointment" class="m-1">Select the appointment you want to cancel</label>')
        self.assertContains(response, '<button type="submit" class="btn btn-mv-green btn-block text-center mt-2 text-white">Cancel Appointment</button>')
        self.assertContains(response, '<h2>All Appointments:</h2>')

    def test_delete_success(self):
        response = self.client.post('/book_appointment/', data={
            'date': '2023-11-13',
            'time': '12:34',
            'details': 'test case appointment',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/cancel_appointment/', data={
            'appointment_id': '1',
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_failure(self):
        response = self.client.post('/book_appointment/', data={
            'date': '2023-11-13',
            'time': '12:34',
            'details': 'test case appointment',
        })
        self.assertEqual(response.status_code, 302)

        # wrong appointment ID
        response = self.client.post('/cancel_appointment/', data={
            'appointment_id': '12',
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_failure_without_appointment(self):
        response = self.client.post('/cancel_appointment/', data={
            'appointment_id': '1',
        })
        self.assertEqual(response.status_code, 200)