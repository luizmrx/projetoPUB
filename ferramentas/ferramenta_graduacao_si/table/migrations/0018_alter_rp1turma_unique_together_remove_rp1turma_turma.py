# Generated by Django 4.1.6 on 2023-11-26 18:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("table", "0017_rp1turma_diaaularp1"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="rp1turma",
            unique_together={("codigo", "cursos", "profs_adicionais", "ano")},
        ),
        migrations.RemoveField(
            model_name="rp1turma",
            name="turma",
        ),
    ]