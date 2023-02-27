# Generated by Django 4.1.7 on 2023-02-27 06:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_post_commentssrc_alter_post_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='_id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='post',
            name='commentsSrc',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
