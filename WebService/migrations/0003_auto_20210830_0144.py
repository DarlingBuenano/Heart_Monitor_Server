# Generated by Django 3.2.6 on 2021-08-30 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebService', '0002_auto_20210826_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bpm',
            name='hora',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='saludcardiaca',
            name='fecha',
            field=models.DateField(),
        ),
    ]
