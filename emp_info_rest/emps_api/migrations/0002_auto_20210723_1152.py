# Generated by Django 3.2.2 on 2021-07-23 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emps_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emppersonal',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterModelTable(
            name='emppersonal',
            table='personal_info',
        ),
    ]
