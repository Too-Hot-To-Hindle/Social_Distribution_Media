# Generated by Django 4.1.7 on 2023-03-12 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_delete_inboxobject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allowlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_addr', models.GenericIPAddressField(blank=True, null=True)),
                ('host', models.URLField(blank=True)),
            ],
        ),
    ]
