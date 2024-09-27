# Generated by Django 5.1.1 on 2024-09-24 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_user_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='educatorprofile',
            options={'verbose_name_plural': 'Educator Profiles'},
        ),
        migrations.AddField(
            model_name='educatorprofile',
            name='bio',
            field=models.CharField(default='', max_length=500),
        ),
    ]
