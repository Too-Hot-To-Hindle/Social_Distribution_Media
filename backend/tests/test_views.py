"""
This test suite ensures each endpoint is alive, taking proper action based
on the request, and returning proper responses.
"""

from django.test import TestCase
from django.urls import reverse
from api.views import Author
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
import base64
import dotenv
import os
import json
dotenv.load_dotenv()


# developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
class TestEndpoints(TestCase):
    
    def setUp(self):
        # Set up the test data
        self.client = APIClient()

        # Create a test user with basic auth credentials
        # self.user = User.objects.create_user(username='testuser', password='testpassword')

        # NOTE: This requires that an .env file is created within this directory (tests) that has a TEST_USERNAME and TEST_PASSWORD
        username = os.getenv("TEST_USERNAME")
        password = os.getenv("TEST_PASSWORD")
        self.user_id = os.getenv("TEST_USER_ID")
        self.credentials = 'Basic ' + base64.b64encode(f'{username}:{password}'.encode('ascii')).decode("ascii")
        self.client.credentials(HTTP_AUTHORIZATION=self.credentials)
        self.client.defaults["HTTP_HOST"]="localhost:3000" # localnode 


    def test_basic_auth(self):
        """ Test that basic auth is working and returns 200"""
        response = self.client.get("/api/authors")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_basic_auth(self):
        """ Test that without basic auth, the endpoint returns 401"""
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get("/api/authors")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=self.credentials) # Reset the credentials

    def test_authors_pagination(self):
        """ Test that the authors endpoint returns the correct number of authors """
        response = self.client.get("/api/authors", {'page': 1, 'size': 1})
        self.assertEqual(len(response.data), 1)

    def test_posts_pagination(self):
        """ Test that the posts endpoint returns the correct number of posts """
        response = self.client.get(f"/api/authors/{self.user_id}/posts", {'page': 1, 'size': 1})
        self.assertEqual(len(response.data), 1)

    def test_post_comments_pagination(self):
        """ Test that the post comments endpoint returns the correct number of comments """
        # create a post
        data = self.client.post(f"/api/authors/{self.user_id}/posts", data=json.dumps({'title': 'TESTING_POST'}), content_type='application/json').json()

        # get author info
        author_info = self.client.get(f"/api/authors/{self.user_id}").json()

        # create 2 comments
        self.client.post(
            f"/api/authors/{self.user_id}/posts/{data['_id']}/comments", 
            data=json.dumps({
                'comment': 'TESTING_COMMENT_1',
                "contentType": "text/plain",
                "author": author_info
            }),
            content_type='application/json'
        )

        self.client.post(
            f"/api/authors/{self.user_id}/posts/{data['_id']}/comments", 
            data=json.dumps({
                'comment': 'TESTING_COMMENT_2',
                "contentType": "text/plain",
                "author": author_info
            }),
            content_type='application/json'
        )

        response = self.client.get(f"/api/authors/{self.user_id}/posts/{data['_id']}/comments", {'page': 1, 'size': 1})
        self.assertEqual(len(response.data), 1)

    def test_inbox_pagination(self):
        """ Test that the inbox endpoint returns the correct number of posts """

        # user should already have 2 posts in their inbox
        response = self.client.get(f"/api/authors/{self.user_id}/inbox", {'page': 1, 'size': 2})
        self.assertEqual(len(response.data['items']), 2)

        response = self.client.get(f"/api/authors/{self.user_id}/inbox", {'page': 1, 'size': 1})
        self.assertEqual(len(response.data['items']), 1)

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