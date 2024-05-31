# Generated by Django 4.1.6 on 2024-05-15 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Discipline",
            fields=[
                (
                    "code",
                    models.CharField(max_length=7, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(default="", max_length=50)),
                ("ideal_semester", models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "num_usp",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=80)),
                ("start_year", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="DisciplineDemand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("currently_studying", models.BooleanField(default=False)),
                ("late", models.BooleanField(default=False)),
                ("year", models.IntegerField()),
                ("semester", models.IntegerField()),
                (
                    "discipline",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="retencao_alunos.discipline",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="retencao_alunos.student",
                    ),
                ),
            ],
        ),
    ]