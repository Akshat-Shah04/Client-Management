# Generated by Django 5.1.4 on 2024-12-21 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_remove_employee_aadhar'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='aadhar',
            field=models.CharField(default='NA', max_length=15),
        ),
    ]