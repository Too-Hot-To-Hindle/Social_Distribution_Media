# Generated by Django 4.1.7 on 2023-03-19 02:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0028_delete_allowedlocalnode_delete_remotenoderequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allowedremotenode',
            name='detail',
        ),
        migrations.RemoveField(
            model_name='allowedremotenode',
            name='host',
        ),
        migrations.RemoveField(
            model_name='allowedremotenode',
            name='ip',
        ),
        migrations.AddField(
            model_name='allowedremotenode',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
