# Generated by Django 4.1.7 on 2023-03-03 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_like_content_type_remove_like_object_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='toAuthor',
            field=models.ForeignKey(default='d294d9dd-225a-44c8-af0f-727c34f282e6', on_delete=django.db.models.deletion.CASCADE, related_name='follow_request_to', to='api.author'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='follow',
            name='fromAuthor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_request_from', to='api.author'),
        ),
        migrations.DeleteModel(
            name='FriendRequest',
        ),
    ]
