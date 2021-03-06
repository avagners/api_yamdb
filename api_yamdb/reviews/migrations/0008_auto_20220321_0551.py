# Generated by Django 3.2.12 on 2022-03-21 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_alter_title_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('-year',)},
        ),
        migrations.RemoveConstraint(
            model_name='title',
            name='unique_name_year',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
