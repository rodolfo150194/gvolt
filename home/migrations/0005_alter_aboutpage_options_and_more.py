# Generated by Django 5.1.1 on 2024-09-06 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_categoriagaleria_custompage_estadisticapage_faqpage_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aboutpage',
            options={'verbose_name': 'Información de la empresa'},
        ),
        migrations.AlterModelOptions(
            name='estadisticapage',
            options={'verbose_name': 'Estadisticas'},
        ),
        migrations.AlterModelOptions(
            name='galeriapage',
            options={'verbose_name': 'Galería', 'verbose_name_plural': 'Galería'},
        ),
    ]
