from django.test import TestCase
from django.urls import reverse
from backend.api.views import Author

# developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
class TestModelAuthor(TestCase):
    @classmethod
    def prepTestData(cls):
        # create fake authors for unit tests
        author_count = 16

        for author_index in range(author_count):
            Author.objects.create(
                displayName = f'CoolBears {author_index}'
            )
    
    def test_url_existence(self):
        response = self.client.get('/authors/')
        self.assertEqual(response.status_code, 200)

    def test_url_access_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)