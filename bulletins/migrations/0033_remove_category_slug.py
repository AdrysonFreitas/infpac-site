# Generated by Django 4.1.3 on 2023-06-17 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulletins', '0032_alter_bulletin_slug_alter_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]
