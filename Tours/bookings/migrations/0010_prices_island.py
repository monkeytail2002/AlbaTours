# Generated by Django 3.1.3 on 2020-12-01 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0009_auto_20201201_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='prices',
            name='island',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
