# Generated by Django 5.0.6 on 2024-11-15 14:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("retencao_alunos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="num_usp",
            field=models.CharField(max_length=12, primary_key=True, serialize=False),
        ),
    ]