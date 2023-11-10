# Generated by Django 4.2.6 on 2023-11-09 21:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('weather_app', '0007_alter_city_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='city',
            unique_together={('owner', 'name')},
        ),
    ]
