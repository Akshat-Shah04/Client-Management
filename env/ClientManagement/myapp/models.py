from django.db import models
from datetime import date


class Employee(models.Model):
    STATUS_CH = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("On Leave", "On Leave"),
    ]

    emp_name = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=20, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS_CH, default="Active")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    mobile = models.BigIntegerField(unique=True, default=1000100010)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20, default="0000")

    def __str__(self):
        return self.emp_name


class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Client(models.Model):
    STATUS_CH = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Pending", "Pending"),
    ]

    clientName = models.CharField(max_length=60)
    status = models.CharField(choices=STATUS_CH, max_length=20, default="Active")
    mobile = models.CharField(max_length=15, unique=True)
    sec_mobile = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=30)
    email = models.EmailField(unique=True, blank=True, null=True)
    referredBy = models.CharField(max_length=50, default="NA")
    services = models.ManyToManyField(Service, through="ClientService")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.clientName

    def total_pending(self):
        # Calculate pending amount for the client
        total_fee = sum(
            client_service.fee for client_service in self.clientservice_set.all()
        )
        return total_fee - self.total_paid()


class ClientService(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    SERV_STATUS = [
        ("Partial Documents Submitted", "Partial Documents Submitted"),
        ("Full Documents Submitted", "Full Documents Submitted"),
        ("Not Started", "Not Started"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Filed", "Filed"),
    ]
    status = models.CharField(
        max_length=100, choices=SERV_STATUS, default="Not Started"
    )
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    billing_date = models.DateField(default=date.today)
    desc = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.service.name} - {self.status} - {self.billing_date}"


class Billing(models.Model):
    clientService = models.ForeignKey(ClientService, on_delete=models.CASCADE)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    billing_date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.clientService.client.clientName} - {self.clientService.service.name} - {self.clientService.service.billing_cycle} - {self.fees} - {self.billing_date}"
