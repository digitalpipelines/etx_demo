# Generated by Django 3.2.16 on 2023-01-25 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_alter_recipeingredientimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeingredientimage',
            name='extracted',
            field=models.JSONField(blank=True, null=True),
        ),
    ]