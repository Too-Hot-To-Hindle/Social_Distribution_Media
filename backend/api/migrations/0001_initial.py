# Generated by Django 4.1.7 on 2023-03-02 04:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.URLField(blank=True, default=None, editable=False)),
                ('url', models.URLField(blank=True, default=None, editable=False)),
                ('host', models.URLField(default='https://social-distribution-media.herokuapp.com', editable=False)),
                ('displayName', models.CharField(max_length=100)),
                ('github', models.URLField(blank=True)),
                ('profileImage', models.URLField(blank=True)),
                ('followers', models.ManyToManyField(blank=True, to='api.author')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('id', models.URLField(blank=True, default=None, editable=False)),
                ('title', models.TextField()),
                ('source', models.URLField(blank=True)),
                ('origin', models.URLField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('contentType', models.TextField(choices=[('text/markdown', 'Common mark'), ('text/plain', 'UTF-8 plain text'), ('application/base64', 'Base 64 string'), ('image/png;base64', 'Base 64 string of PNG image'), ('image/jpeg;base64', 'Base 64 string of JPEG image')], default='text/plain')),
                ('content', models.TextField(blank=True)),
                ('categories', models.JSONField(blank=True, default=list)),
                ('count', models.IntegerField(default=0, editable=False)),
                ('comments', models.URLField(blank=True)),
                ('commentsSrc', models.JSONField(blank=True, default=dict)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('visibility', models.TextField(choices=[('PUBLIC', 'Public'), ('FRIENDS', 'Friends')], default='FRIENDS')),
                ('unlisted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.author')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('summary', models.TextField()),
                ('object_id', models.UUIDField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.author')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='InboxObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField()),
                ('object_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.author')),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_request_from', to='api.author')),
                ('to_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_request_to', to='api.author')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fromAuthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.URLField(blank=True, default=None, editable=False)),
                ('comment', models.TextField()),
                ('contentType', models.TextField(choices=[('text/markdown', 'Common mark'), ('text/plain', 'UTF-8 plain text')])),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.post')),
            ],
        ),
    ]
