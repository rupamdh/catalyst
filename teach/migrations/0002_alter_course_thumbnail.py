# Generated by Django 5.1.1 on 2024-09-24 07:33

import teach.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teach', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='thumbnail',
            field=models.ImageField(upload_to=teach.models.rename_image),
        ),
    ]
