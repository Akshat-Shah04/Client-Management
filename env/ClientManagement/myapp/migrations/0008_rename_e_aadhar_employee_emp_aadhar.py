# Generated by Django 5.1.4 on 2024-12-21 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_rename_aadhar_employee_e_aadhar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='e_aadhar',
            new_name='emp_aadhar',
        ),
    ]
