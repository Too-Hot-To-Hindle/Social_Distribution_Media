# Generated by Django 4.1.7 on 2023-02-26 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_remove_post_commentssrc'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='commentsSrc',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.JSONField(default=list),
        ),
    ]