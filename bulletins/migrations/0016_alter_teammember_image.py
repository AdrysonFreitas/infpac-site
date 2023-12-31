# Generated by Django 4.1.3 on 2023-06-07 05:25

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('bulletins', '0015_alter_teammember_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='img/team/default.png', force_format='JPEG', help_text='Formato: 300x300', keep_meta=True, quality=[100, 100], scale=None, size=[300, 300], upload_to='img/team/', verbose_name='Foto'),
        ),
    ]
