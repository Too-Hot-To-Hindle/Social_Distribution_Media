from django.test import TestCase
from backend.api.models import Author

# developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
class TestModelAuthor(TestCase):
    @classmethod
    def prepTestData(cls):
        Author.objects.create(
            displayName = 'CoolBears'
        )
    
    def test_display_name(self):
        my_author = Author.objects.get(id=1)
        field_value = my_author._meta.get_field('displayName').verbose_name
        self.assertEqual(field_value, 'displayName')