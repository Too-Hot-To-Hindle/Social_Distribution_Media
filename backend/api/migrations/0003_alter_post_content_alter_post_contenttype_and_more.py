# Generated by Django 4.1.7 on 2023-02-26 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_author__id_alter_author_displayname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='contentType',
            field=models.TextField(choices=[('text/markdown', 'Common mark'), ('text/plain', 'UTF-8 plain text'), ('application/base64', 'Base 64 string'), ('image/png;base64', 'Base 64 string of PNG image'), ('image/jpeg;base64', 'Base 64 string of jpeg image')], default='text/plain'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
