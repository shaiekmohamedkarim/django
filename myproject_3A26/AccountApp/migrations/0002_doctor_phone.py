from django.core.validators import RegexValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("AccountApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="phone",
            field=models.CharField(
                default="00000000",
                max_length=8,
                validators=[
                    RegexValidator(
                        message="Le téléphone doit contenir exactement 8 chiffres.",
                        regex=r"^\d{8}$",
                    )
                ],
            ),
            preserve_default=False,
        ),
    ]
