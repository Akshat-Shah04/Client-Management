# Generated by Django 5.1.4 on 2024-12-30 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_rename_fees_billing_fees_recieved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='fee_status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'), ('Discounted', 'Discounted'), ('Partial', 'Partial')], default='Unpaid', max_length=50, null=True),
        ),
    ]