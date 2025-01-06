from django.db import models
from datetime import date


class Employee(models.Model):
    POSITION = [
        ("Admin", "Admin"),
        ("Staff", "Staff"),
    ]
    emp_name = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=20, decimal_places=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    mobile = models.BigIntegerField(unique=True, default=1000100010)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20, default="0000")
    position = models.CharField(max_length=25, choices=POSITION, default="Staff")

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

    # def total_paid(self):
    #     # Sum up all the fees_received for the related Billing records
    #     return sum(billing.fees_recieved for billing in self.billing_set.all())


class Billing(models.Model):
    clientService = models.ForeignKey(ClientService, on_delete=models.CASCADE)
    fees_recieved = models.DecimalField(max_digits=10, decimal_places=2)
    billing_date = models.DateField(default=date.today)
    STATUS = [
        ("Paid", "Paid"),
        ("Unpaid", "Unpaid"),
        ("Discounted", "Discounted"),
        ("Partial", "Partial"),
    ]
    fee_status = models.CharField(
        max_length=50, choices=STATUS, blank=False, default="Unpaid", null=True
    )
    PAY = [
        ("UPI", "UPI"),
        ("Cash", "Cash"),
        ("Check", "Check"),
        ("Netbanking", "Netbanking"),
    ]
    payment_type = models.CharField(choices=PAY, max_length=20, blank=True)
    outstanding_amt = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return (
            f"{self.clientService.client.clientName} - "
            f"{self.clientService.service.name} - "
            # f"{self.clientService.service.billing_cycle} - "
            f"{self.fees_recieved} - "
            f"{self.billing_date}"
        )


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    STATUS = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("On Leave", "On Leave"),
    ]
    status = models.CharField(choices=STATUS, max_length=20)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    is_late = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee.emp_name} - {self.date} - {self.status}"


class Task(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="assigned_tasks"
    )
    assigned_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    progress = models.TextField(
        blank=True, null=True
    )  # To store employee's progress notes

    def __str__(self):
        return f"{self.title} - {self.status}"
