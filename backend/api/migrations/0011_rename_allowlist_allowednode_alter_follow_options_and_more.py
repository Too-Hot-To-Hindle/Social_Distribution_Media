# Generated by Django 4.1.7 on 2023-03-12 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_allowlist'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Allowlist',
            new_name='AllowedNode',
        ),
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name_plural': 'Follow Requests'},
        ),
        migrations.AlterModelOptions(
            name='inbox',
            options={'verbose_name_plural': 'Inboxes'},
        ),
    ]
