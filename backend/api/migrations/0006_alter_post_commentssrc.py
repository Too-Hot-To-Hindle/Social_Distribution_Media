# Generated by Django 4.1.7 on 2023-02-26 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_post_commentssrc_alter_post_contenttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='commentsSrc',
            field=models.JSONField(blank=True, default={}),
            preserve_default=False,
        ),
    ]
