# Generated by Django 3.1.3 on 2020-11-30 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_auto_20201129_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='islands',
            name='am_arrival',
            field=models.CharField(max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='islands',
            name='am_depart',
            field=models.CharField(max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='islands',
            name='pm_arrival',
            field=models.CharField(max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='islands',
            name='pm_depart',
            field=models.CharField(max_length=9, null=True),
        ),
    ]