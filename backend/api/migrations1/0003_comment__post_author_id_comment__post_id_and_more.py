# Generated by Django 4.1.7 on 2023-03-02 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_comment_post_alter_comment_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='_post_author_id',
            field=models.UUIDField(blank=True, default='d294d9dd-225a-44c8-af0f-727c34f282e6'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='_post_id',
            field=models.UUIDField(blank=True, default='d294d9dd-225a-44c8-af0f-727c34f282e6'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.URLField(blank=True, default=None),
        ),
    ]