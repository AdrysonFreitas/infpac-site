# Generated by Django 4.1.3 on 2023-06-07 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletins', '0019_alter_partner_image_alter_teammember_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='link',
            field=models.CharField(default='lattes.com', max_length=200, verbose_name='Lattes'),
            preserve_default=False,
        ),
    ]
