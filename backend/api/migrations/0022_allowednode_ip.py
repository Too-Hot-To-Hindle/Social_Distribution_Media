# Generated by Django 4.1.7 on 2023-03-16 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_remove_allowednode_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='allowednode',
            name='ip',
            field=models.GenericIPAddressField(blank=True, editable=False, null=True),
        ),
    ]
