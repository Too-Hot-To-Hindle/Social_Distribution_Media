# Generated by Django 4.1.7 on 2023-03-03 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_fromauthor_follow_actor_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InboxObject',
        ),
    ]
