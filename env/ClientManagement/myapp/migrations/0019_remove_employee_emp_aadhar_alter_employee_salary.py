# Generated by Django 5.1.4 on 2024-12-23 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_rename_aadhar_client_sec_mobile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='emp_aadhar',
        ),
        migrations.AlterField(
            model_name='employee',
            name='salary',
            field=models.DecimalField(decimal_places=0, max_digits=20),
        ),
    ]
