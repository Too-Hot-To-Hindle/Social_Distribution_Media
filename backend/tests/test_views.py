"""
This test suite ensures each endpoint is alive, taking proper action based
on the request, and returning proper responses.
"""

from django.test import TestCase
from django.urls import reverse
from api.views import Author
from django.contrib.auth.models import User

# developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
class TestEndpoints(TestCase):
    
    def setUp(self):
        pass

    def test_get_all_authors(self):
        """ """
        # resp = self.client.post('/api/authors', {'username': 'testuser12345', 'password': 'testpwd'})
        # print(resp)
        # user = User.objects.create_user('test_user', password='testpwd')
        # print(self.client.login())
        # print(self.client.force_login(user))
        # response = self.client.get('/api/authors', {'name': 'test_usre', 'passwd': 'testpwd'})
        # print(response)
        # self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)
    
    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)
    
    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)
    
    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)
    
    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)
    
    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)
    
    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_(self):
    #     """ """
    #     response = self.client
    #     self.assertEqual(response.status_code, 200)

    # def test_url_existence(self):
    #     response = self.client.get('/authors')
    #     self.assertEqual(response.status_code, 200)

    # def test_url_access_by_name(self):
    #     response = self.client.get(reverse('authors'))
    #     self.assertEqual(response.status_code, 200)