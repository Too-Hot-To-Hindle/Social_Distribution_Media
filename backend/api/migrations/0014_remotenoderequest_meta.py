# Generated by Django 4.1.7 on 2023-03-13 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_remotenoderequest_allowednode_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='remotenoderequest',
            name='meta',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
