# Generated by Django 4.1.7 on 2023-03-17 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_alter_author_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.URLField(blank=True, default=None),
        ),
    ]