from django.test import TestCase, Client

readonly_fields = ['username','first_name', 'last_name', 'phone','email']
ClientNavBar_Fields = ["MedVoyage", "About", "Contact", "Profile","Sign Out"]

class ClientProfileTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_client_Profile_content(self):
        response = self.client.get('/client_profile/')
        self.assertEqual(response.status_code, 200)
        #navbar
        for nav_field in ClientNavBar_Fields:
            self.assertContains(response, nav_field)
        #footer
        self.assertContains(response, "&copy; MedVoyage")
        #content
        self.assertContains(response, '<h2 class="text-center">Your Information</h2>') 
        #links
        self.assertContains(response, '<a href="/client_update/" class="btn btn-link">Edit</a>')
    
    
    def test_client_profile_rendered_correctly(self):
        response = self.client.get('/client_profile/') 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clientprofile.html')
        # checking the form elements
        self.assertContains(response, 'id_username')
        self.assertContains(response, 'id_firstname')
        self.assertContains(response, 'id_lastname')
        self.assertContains(response, 'id_email')
        self.assertContains(response, 'id_phone')
        
    def test_client_profile_labels(self):
        response = self.client.get('/client_profile/')  
        self.assertEqual(response.status_code, 200)
        #checking the labels
        self.assertContains(response, '<label for="id_username">Username:</label>')
        self.assertContains(response, '<label for="id_firstname">First Name:</label>')
        self.assertContains(response, '<label for="id_lastname">Last Name:</label>')
        self.assertContains(response, '<label for="id_phone">Phone Number:</label>')
        self.assertContains(response, '<label for="id_email">Email:</label>')
        
    def test_readonly_fields(self):
        response = self.client.get('/client_profile/')
        self.assertEqual(response.status_code, 200)
        for fields in readonly_fields:
            self.assertContains(response, fields)

    
    