# Generated by Django 5.1 on 2025-01-01 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0029_alter_billing_fee_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='outstanding_amt',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='billing',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('UPI', 'UPI'), ('Cash', 'Cash'), ('Check', 'Check'), ('Netbanking', 'Netbanking')], max_length=20),
        ),
    ]
