# Generated by Django 4.1.7 on 2023-03-03 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_inbox_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='author_following', to='api.author'),
        ),
        migrations.AlterField(
            model_name='author',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='author_followers', to='api.author'),
        ),
    ]