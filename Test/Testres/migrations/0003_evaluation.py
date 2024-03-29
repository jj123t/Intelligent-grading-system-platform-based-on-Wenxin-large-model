# Generated by Django 4.1 on 2024-03-17 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Testres", "0002_fileinfo_imageupload"),
    ]

    operations = [
        migrations.CreateModel(
            name="Evaluation",
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
                (
                    "evaluator_type",
                    models.CharField(
                        choices=[("S", "学生自我评价"), ("T", "教师评价")],
                        max_length=1,
                        verbose_name="评价类型",
                    ),
                ),
                ("comment", models.TextField(verbose_name="评价内容")),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evaluations",
                        to="Testres.student",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evaluations",
                        to="Testres.record",
                    ),
                ),
            ],
        ),
    ]
