# Generated by Django 4.1.7 on 2023-03-13 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_rename_ip_addr_allowednode_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemoteNodeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('host', models.URLField(blank=True)),
                ('detail', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='allowednode',
            name='detail',
            field=models.TextField(blank=True),
        ),
    ]