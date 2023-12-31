# Generated by Django 4.1.3 on 2023-06-01 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletins', '0008_alter_bulletin_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.CharField(blank=True, max_length=300, verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='image',
            field=models.CharField(default='https://i.postimg.cc/vTWkBNj5/default-partner.png', max_length=300, verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='image',
            field=models.CharField(blank=True, max_length=300, verbose_name='Foto'),
        ),
    ]
