from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

SERVICE_ADDRESS = "https://social-distribution-media.herokuapp.com"
PREFIX = 'api'
API_BASE = f"{SERVICE_ADDRESS}/{PREFIX}"

class Author(models.Model):

    type = 'author'

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.URLField(blank=True, default=None, editable=False)
    url = models.URLField(blank=True, default=None, editable=False)
    host = models.URLField(default=SERVICE_ADDRESS, editable=False)
    displayName = models.CharField(max_length=100)
    github = models.URLField(blank=True)
    profileImage = models.URLField(blank=True)
    # https://stackoverflow.com/questions/35957837/trying-to-make-a-postgresql-field-with-a-list-of-foreign-keys-in-django
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ManyToManyField.symmetrical
    # NOTE: Can't specify on_delete for this, but the default behaviour is CASCADE which is correct for us :)
    followers = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return self.displayName
    
    def save(self, *args, **kwargs) -> None:
        # Set the id and url fields intially, using the generated id.
        if not self.id:
            self.id = f"{API_BASE}/authors/{self._id}"
        if not self.url:
            self.url = f"{SERVICE_ADDRESS}/authors/{self._id}"
        return super().save(*args, **kwargs)

class Follower:
    def __init__(self):
        pass

class Post(models.Model):

    PUBLIC = 'PUBLIC'
    FRIENDS = 'FRIENDS'

    MARKDOWN = 'text/markdown'
    PLAINTEXT = 'text/plain'
    BASE64 = 'application/base64'
    BASE64_PNG = 'image/png;base64'
    BASE64_JPEG = 'image/jpeg;base64'

    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (FRIENDS, 'Friends')
    ]

    CONTENT_TYPES = [
        (MARKDOWN, 'Common mark'),
        (PLAINTEXT, 'UTF-8 plain text'),
        (BASE64, 'Base 64 string'),
        (BASE64_PNG, 'Base 64 string of PNG image'),
        (BASE64_JPEG, 'Base 64 string of JPEG image'),
    ]

    type = 'post'

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4)  # Editable for the PUT endpoint
    id = models.URLField(blank=True, default=None, editable=False)
    title = models.TextField()
    source = models.URLField(blank=True)  # Need to clarify source and origin fields
    origin = models.URLField(blank=True)
    description = models.TextField(blank=True)
    contentType = models.TextField(choices=CONTENT_TYPES, default=PLAINTEXT)
    content = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.JSONField(default=list, null=False, blank=True)
    count = models.IntegerField(default=0, editable=False)
    comments = models.URLField(blank=True)
    commentsSrc = models.JSONField(default=dict, null=False, blank=True)
    published = models.DateTimeField(auto_now_add=True)  # Sets to timezone.now on first creation
    visibility = models.TextField(choices=VISIBILITY_CHOICES, default=FRIENDS)
    unlisted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs) -> None:
        # Set the id and url fields intially, using the generated id.
        if not self.id:
            self.id = f"{API_BASE}/authors/{self.author._id}/posts/{self._id}"
            self.comments = f"{self.id}/comments"
        return super().save(*args, **kwargs)

class Comment:
    def __init__(self):
        pass

class Inbox:
    def __init__(self):
        pass