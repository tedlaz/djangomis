# Generated by Django 3.0.7 on 2020-07-16 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apodoxestypeefka',
            name='plirotees',
            field=models.BooleanField(default=True, verbose_name='Αποδοχές πληρωτέες'),
        ),
    ]
