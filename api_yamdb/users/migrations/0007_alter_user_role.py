# Generated by Django 3.2.12 on 2022-03-19 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.TextField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='USER'),
        ),
    ]
