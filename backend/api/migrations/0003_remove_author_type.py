# Generated by Django 4.1.7 on 2023-02-21 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_author_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='type',
        ),
    ]