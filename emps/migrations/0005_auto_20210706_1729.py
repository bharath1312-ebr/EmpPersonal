# Generated by Django 3.2.2 on 2021-07-06 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emps', '0004_auto_20210706_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emppersonal',
            name='otp',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='emppersonal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
