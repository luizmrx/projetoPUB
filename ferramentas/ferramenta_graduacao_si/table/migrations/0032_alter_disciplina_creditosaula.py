# Generated by Django 5.0.6 on 2025-02-23 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0031_alter_disciplina_tipodisc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disciplina',
            name='CreditosAula',
            field=models.IntegerField(choices=[(0, 0), (2, 2), (4, 4)], default=4),
        ),
    ]
