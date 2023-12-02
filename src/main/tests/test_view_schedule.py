# from django.test import TestCase, Client

# NavBar_Fields = ["MedVoyage", "About", "Contact", "Login/Signup"]

# class ViewScheduleTestCases(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_view_schedule_content():
#         response = self.client.get('/view_schedule/')
#         self.assertEqual(response.status_code, 200)

#         self.assertContains(response, "MedVoyage | View Schedule")
#         self.assertEqual(response.status_code, 200)

#         for nav_field in NavBar_Fields:
#             self.assertContains(response, nav_field)
        
#         self.assertContains(response, "<p>&copy; MedVoyage</p>")

#         self.assertContains(response, '<h3>Select the date you\'d like to see appointments for:</h3>')
#         self.assertContains(response, 'input type="submit" value="View"')

#     def test_view_success(self):
#         response = self.client.post('/book_appointment/', data={
#             'date': '2023-11-13',
#             'time': '12:34',
#             'details': 'test case appointment',
#         })
#         self.assertEqual(response.status_code, 200)

#         response = self.client.post('/view_schedule/', data={
#             'date': '2023-11-13',
#         })
#         self.assertEqual(response.status_code, 200)