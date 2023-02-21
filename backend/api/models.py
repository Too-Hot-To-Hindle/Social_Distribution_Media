from django.db import models
import uuid

# Create your models here.

class Author(models.Model):

    type = 'author'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.URLField()
    display_name = models.CharField(max_length=200)
    url = models.URLField()
    github = models.URLField()
    profile_image = models.URLField()

    def __str__(self):
        return self.display_name

class Follower:
    def __init__(self):
        pass

class Post:
    def __init__(self):
        pass

class Comment:
    def __init__(self):
        pass

class Inbox:
    def __init__(self):
        pass