from django.test import TestCase, Client

ClientNavBar_Fields = ["MedVoyage", "About", "Contact", "Profile","Sign Out"]

class ContactUsTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_client_dashboard_content(self):
        response = self.client.get('/client_dashboard/')
        self.assertEqual(response.status_code, 200)
        #navbar
        for nav_field in ClientNavBar_Fields:
            self.assertContains(response, nav_field)
        #footer
        self.assertContains(response, "&copy; MedVoyage")
        #content
        self.assertContains(response, '<h1 class="display-2 display-md-3 display-lg-4" style="color: #333;font-weight: bold;">Welcome to your Dashboard</h1>') 
        
