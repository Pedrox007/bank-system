# Generated by Django 4.2.1 on 2023-05-13 19:09

import apps.resources.base_model
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_managers_user_groups_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', apps.resources.base_model.CustomUserManager()),
            ],
        ),
    ]
