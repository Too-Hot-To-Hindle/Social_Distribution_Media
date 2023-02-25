from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

# Create your models here.

class Author(models.Model):

    type = 'author'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.URLField()
    displayName = models.CharField(max_length=100, default=None)
    url = models.URLField()
    github = models.URLField()
    profileImage = models.URLField()
    
    # https://stackoverflow.com/questions/35957837/trying-to-make-a-postgresql-field-with-a-list-of-foreign-keys-in-django
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ManyToManyField.symmetrical
    # NOTE: Can't specify on_delete for this, but the default behaviour is CASCADE which is correct for us :)
    followers = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return self.displayName

class Follower:
    def __init__(self):
        pass

class Post:

    VISIBILITY_CHOICES = [
        ('PUBLIC', 'Public'),
        ('FRIENDS', 'Friends')
    ]

    id = models.URLField(primary_key=True, default="", editable=False)  # TODO: Change this
    type = models.TextField()
    title = models.CharField(max_length=100)
    source = models.URLField()
    origin = models.URLField()
    description = models.CharField(max_length=200)
    contentType = models.CharField(max_length=20)
    content = models.TextField()  # No max length  compared to CharField
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    categories = models.JSONField()
    count = models.IntegerField()
    comments = models.URLField()
    commentsSrc = models.JSONField()  # idk
    published = models.DateTimeField()
    visibility = models.TextField(choices=VISIBILITY_CHOICES, default='FRIENDS')
    unlisted = models.BooleanField(default=False)

class Comment:
    def __init__(self):
        pass

class Inbox:
    def __init__(self):
        pass