# Generated by Django 5.1.1 on 2024-10-01 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
