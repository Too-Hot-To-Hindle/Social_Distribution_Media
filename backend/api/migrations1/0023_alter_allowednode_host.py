# Generated by Django 4.1.7 on 2023-03-16 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_allowednode_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allowednode',
            name='host',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]