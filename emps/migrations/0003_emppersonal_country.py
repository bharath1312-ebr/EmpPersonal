# Generated by Django 3.2.2 on 2021-06-24 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emps', '0002_alter_emppersonal_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='emppersonal',
            name='country',
            field=models.CharField(default='India', max_length=25),
        ),
    ]
