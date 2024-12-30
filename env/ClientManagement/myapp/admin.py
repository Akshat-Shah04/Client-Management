from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Service)
admin.site.register(Billing)
admin.site.register(ClientService)
