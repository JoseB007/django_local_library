# Generated by Django 5.0.6 on 2024-06-02 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_genre_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'No disponible'), ('o', 'En prestamo'), ('a', 'Disponibel'), ('r', 'Reservado')], default='m', help_text='Disponibilidad del libro', max_length=1),
        ),
    ]