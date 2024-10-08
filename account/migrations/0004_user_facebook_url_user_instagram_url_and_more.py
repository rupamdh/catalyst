# Generated by Django 5.1.1 on 2024-09-24 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='facebook_url',
            field=models.URLField(blank=True, null=True, verbose_name='Facebook profile URL'),
        ),
        migrations.AddField(
            model_name='user',
            name='instagram_url',
            field=models.URLField(blank=True, null=True, verbose_name='Instagram profile URL'),
        ),
        migrations.AddField(
            model_name='user',
            name='linkedin_url',
            field=models.URLField(blank=True, null=True, verbose_name='LinkedIn profile URL'),
        ),
        migrations.AddField(
            model_name='user',
            name='twitter_url',
            field=models.URLField(blank=True, null=True, verbose_name='Twitter profile URL'),
        ),
    ]
