# Generated by Django 5.1.1 on 2024-09-24 11:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teach', '0003_alter_course_off_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 9, 24, 11, 26, 20, 690472, tzinfo=datetime.timezone.utc)),
        ),
    ]
