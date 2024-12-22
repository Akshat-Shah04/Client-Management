from django.db import models

class Employee(models.Model):
    STATUS_CH = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("On Leave", "On Leave"),
    ]

    emp_name = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS_CH, default="Active")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    emp_aadhar = models.CharField(default='NA',blank=True,null=True,max_length=15)
    mobile = models.BigIntegerField(unique=True,default=1000100010)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20,default='0000')
    def __str__(self):
        return self.emp_name


class Service(models.Model):
    name = models.CharField(max_length=100)
    # price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Client(models.Model):
    STATUS_CH = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Pending", "Pending"),
    ]

    clientName = models.CharField(max_length=60)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CH, max_length=20, default="Active")
    pan = models.CharField(max_length=15, unique=True)
    aadhar = models.CharField(max_length=15, unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    referredBy = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="referrals")
    services = models.ManyToManyField(Service, through="ClientService")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.clientName

    def total_paid(self):
        # Calculate total amount paid by the client
        payments = Payment.objects.filter(client=self)
        return sum(payment.amount for payment in payments)

    def total_pending(self):
        # Calculate pending amount for the client
        total_fee = sum(
            client_service.fee for client_service in self.clientservice_set.all()
        )
        return total_fee - self.total_paid()


class ClientService(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.client.clientName} - {self.service.name} - {self.fee}"


class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} from {self.client.clientName} on {self.payment_date}"
