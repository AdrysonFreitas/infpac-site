# Generated by Django 4.1.3 on 2023-06-17 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletins', '0024_bulletin_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]