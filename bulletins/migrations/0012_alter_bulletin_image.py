# Generated by Django 4.1.3 on 2023-06-07 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletins', '0011_remove_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='image',
            field=models.ImageField(upload_to='img/bulletins/', verbose_name='Imagem'),
        ),
    ]
