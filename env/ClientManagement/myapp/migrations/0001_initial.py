# Generated by Django 5.1.4 on 2024-12-20 11:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('salary', models.DecimalField(decimal_places=0, max_digits=10)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('On Leave', 'On Leave')], default='Active', max_length=20)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientName', models.CharField(max_length=40)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('pan', models.CharField(max_length=10, unique=True)),
                ('aadhar', models.CharField(max_length=12, unique=True)),
                ('mobile', models.CharField(max_length=13, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('referredBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referrals', to='myapp.client')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.client')),
            ],
        ),
        migrations.CreateModel(
            name='ClientService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.client')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.service')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='services',
            field=models.ManyToManyField(through='myapp.ClientService', to='myapp.service'),
        ),
    ]