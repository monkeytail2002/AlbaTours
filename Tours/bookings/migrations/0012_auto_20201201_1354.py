# Generated by Django 3.1.3 on 2020-12-01 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0011_auto_20201201_0025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booked',
            name='booked_day',
        ),
        migrations.RemoveField(
            model_name='booked',
            name='prices_id',
        ),
        migrations.AddField(
            model_name='booked',
            name='adults',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='booked',
            name='children',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='booked',
            name='wheelchair_needed',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
