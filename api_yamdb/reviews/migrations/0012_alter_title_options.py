# Generated by Django 3.2.12 on 2022-03-21 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_auto_20220321_0841'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['category', 'name', 'year']},
        ),
    ]