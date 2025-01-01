from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from datetime import date
from django.db.models import Sum
from django.core.mail import send_mail
from django.utils.timezone import now
from decimal import Decimal

# Create your views here.


def signup(request):
    if request.method == "POST":
        emp_name = request.POST["emp_name"]
        salary = request.POST["salary"]
        emp_aadhar = request.POST.get("emp_aadhar", "NA")
        mobile = request.POST["mobile"]
        email = request.POST["email"]
        status = "Active"
        password = request.POST["password"]

        try:
            # Check for duplicate email or mobile
            if Employee.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
                return redirect("signup")
            if Employee.objects.filter(mobile=mobile).exists():
                messages.error(request, "Mobile number is already registered.")
                return redirect("signup")

            Employee.objects.create(
                emp_name=emp_name,
                salary=salary,
                status=status,
                emp_aadhar=emp_aadhar,
                mobile=mobile,
                email=email,
                password=password,
            )

            messages.success(request, "Sign-up successful. Please login.")
            print("Sign-up successful. Please login.")

            return redirect("login")  # Redirect to login page

        except Exception as e:
            messages.error(request, f"Error during sign-up: {e}")
            return redirect("signup")
    else:
        return render(request, "signup.html")


def login(request):
    if request.method == "POST":
        try:
            employee = Employee.objects.get(email=request.POST["email"])
            if employee.password == request.POST["password"]:
                request.session["email"] = employee.email
                request.session["emp_name"] = employee.emp_name
                print("Login Is Successful")
                return render(request, "dashboard.html")  # Redirects to dashboard
            else:
                msg = "Invalid Credentials"
                return render(request, "login.html", {"msg": msg})
        except Employee.DoesNotExist:
            msg = "Employee not found"
            return render(request, "login.html", {"msg": msg})
        except Exception as e:
            print(e)
            msg = "Error Logging In..."
            return render(request, "login.html", {"msg": msg})
    else:
        # For GET requests
        return render(request, "login.html")


def header(request):
    client = Client.objects.all()
    return render(request, "header.html", {"clients": client})


def logout(request):
    # Clear session data
    request.session.flush()
    return redirect("login")


def dashboard(request):
    client = Client.objects.all()
    return render(request, "dashboard.html", {"clients": client})


def add_client(request):
    if request.method == "POST":
        try:
            # Create a new client
            client = Client.objects.create(
                clientName=request.POST["clientName"],
                mobile=request.POST["mobile"],
                sec_mobile=request.POST["sec_mobile"],
                city=request.POST["city"],
                referredBy=request.POST["referredBy"],
                email=request.POST.get("email", None),
            )

            """
            # Get selected service IDs from the POST data
            service_ids = request.POST.getlist("services")
            for service_id in service_ids:
                service = Service.objects.get(id=service_id)
                ClientService.objects.create(
                    service=service,
                    client=client,
                    fee=0,  # Set fee to 0 or another default value
                )
            """
            messages.success(request, "Client created successfully.")
            return redirect("dashboard")  # Redirect to the dashboard or another page

        except Exception as e:
            print(">" * 30, " Error Occurred >>>>> add_client >>>>>", e)
            messages.error(request, f"An error occurred: {e}")
            return render(request, "add_client.html")
    else:
        # Render the form with available s+ervices
        services = Service.objects.all()
        return render(request, "add_client.html", {"services": services})


def update_client(request, pk):
    client = Client.objects.get(pk=pk)
    services = Service.objects.all()

    if request.method == "POST":
        # Update client fields
        client.clientName = request.POST["clientName"]
        client.mobile = request.POST["mobile"]
        client.sec_mobile = request.POST["sec_mobile"]
        client.city = request.POST["city"]
        client.email = request.POST.get("email", None)
        client.referredBy = request.POST.get("referredBy", None)

        # Update Many-to-Many Services (if applicable)
        selected_services = request.POST.getlist("services")  # Get selected services
        client.services.set(selected_services)  # Update services

        try:
            client.save()
            messages.success(request, "Client Updated Successfully")
            return redirect("dashboard")
        except Exception as e:
            print(">" * 30, "Error Occurred >>> update_client >>>", e)
            messages.error(request, "Failed to update client. Please try again.")
            return render(
                request, "update_client.html", {"client": client, "services": services}
            )
    else:
        return render(
            request, "update_client.html", {"client": client, "services": services}
        )


def delete_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
        ClientService.objects.filter(client=client).delete()
        client.delete()
        messages.success(request, "Client deleted successfully.")
        return redirect("dashboard")
    except Exception as e:
        print(">>>>>>>>> Error Occurred >>> delete_client >>>", e)
        messages.error(request, "Failed to delete client. Please try again.")
        return redirect("dashboard")


def clients(request):
    query = request.GET.get("q", "")
    if query:
        clients = (
            Client.objects.filter(clientName__icontains=query)
            | Client.objects.filter(mobile__icontains=query)
            | Client.objects.filter(sec_mobile__icontains=query)
        )

    else:
        clients = Client.objects.all()

    client_data = []
    for client in clients:
        services = ClientService.objects.filter(client=client)
        client_data.append(
            {
                "client": client,
                "services": services,
            }
        )

    return render(request, "clients.html", {"client_data": client_data, "query": query})


def add_clientservice(request, pk):
    client = get_object_or_404(Client, pk=pk)
    services = Service.objects.all()
    status_choices = ClientService.SERV_STATUS

    if request.method == "POST":
        selected_services = request.POST.getlist("services")
        for service_id in selected_services:
            service = get_object_or_404(Service, pk=service_id)

            fee = request.POST.get(f"fee_{service.id}")
            desc = (
                request.POST.get(f"desc_{service.id}") or "NA"
            )  # Default to "NA" if not provided
            status = request.POST.get(f"status_{service.id}")
            billing_date = (
                request.POST.get(f"billing_date_{service.id}") or date.today()
            )
            print(desc)
            # Save client service (Description is optional)
            ClientService.objects.create(
                client=client,
                service=service,
                fee=fee,
                desc=desc,
                status=status,
                billing_date=billing_date,
            )

        return redirect("clients")

    return render(
        request,
        "add_clientservice.html",
        {"client": client, "services": services, "status_choices": status_choices},
    )


def delete_clientservice(request, pk):
    try:
        ClientService.objects.filter(pk=pk).delete()
        print("Delete Successfull >>>> >>>>> >>>>>> >>>>")
        return redirect("clients")
    except Exception as e:
        print(f">>>>> Error Occurred >>>>> Delete ClientService >>>>> {pk} >>>>> !!!")
        return redirect("dashboard")


def update_clientservice(request, pk):
    # Fetch the client and their services
    client = get_object_or_404(Client, pk=pk)
    client_services = ClientService.objects.filter(client=client)
    services = Service.objects.all()  # Available services
    status_choices = ClientService.SERV_STATUS  # Status choices defined in the model
    print(">>>>>>>>>> ERror 1 >>>>>>>>>>")
    if request.method == "POST":
        # Iterate through submitted services and update each record
        print(">>>>>>>>> Error 2 >>>>>>>>")
        for service in client_services:
            fee = request.POST.get(f"fee_{service.id}")
            status = request.POST.get(f"status_{service.id}")
            billing_date = (
                request.POST.get(f"billing_date_{service.id}") or date.today()
            )
            print(">>>>>>>>Error 3>>>>>>>>>>>")
            desc = request.POST.get(f"desc_{service.id}") or "NA"
            # Update service fields
            service.fee = float(fee) if fee else service.fee
            service.status = status
            service.billing_date = billing_date
            print(">>>>>>>>>>>> Error 4 >>>>>>>>>>>>c")
            service.save()
            print(">>>>>>>>>>>> Error 5 >>>>>>>>>>>>")
            print(desc)
        return redirect("clients")  # Redirect to the client list page

    return render(
        request,
        "update_clientservice.html",
        {
            "client": client,
            "services": client_services,
            "status_choices": status_choices,
        },
    )


def view_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client_services = ClientService.objects.filter(client=client)

    # Aggregate fees for billing summary
    total_fees = client_services.aggregate(total_fees=Sum("fee"))["total_fees"] or 0
    total_received = (
        Billing.objects.filter(clientService__in=client_services).aggregate(
            total_received=Sum("fees_recieved")
        )["total_received"]
        or 0
    )
    total_pending = total_fees - total_received

    context = {
        "client": client,
        "client_services": client_services,
        "billing": Billing.objects.filter(clientService__in=client_services),
        "total_fees": total_fees,
        "total_received": total_received,
        "total_pending": total_pending,
    }
    return render(request, "view_client.html", context)


def add_service(request):
    if request.method == "POST":
        service = Service.objects.create(name=request.POST["name"])
        return redirect("dashboard")
    else:
        service_list = Service.objects.all()
        return render(request, "add_service.html", {"service_list": service_list})


def view_service(request):
    try:
        service = Service.objects.all()
        print(service)
        return render(request, "view_service.html", {"service": service})
    except Exception as e:
        print("View Exception Occ >>>> ", e)
        return render(request, "view_service.html")


def delete_service(request, pk):
    try:
        service = Service.objects.get(pk=pk)
        service.delete()
        print("Service deleted >>>>>> ")
        return redirect("dashboard")
    except Exception as e:
        print("Exception Occured >>> ", e)
        return render(request, "view_service.html")


# def generate_bill(request, pk):
#     client = get_object_or_404(Client, pk=pk)
#     client_services = ClientService.objects.filter(client=client, status="Completed")

#     # Check if there are any services for the client
#     if not client_services:
#         messages.error(request, "No completed services found for this client.")
#         return redirect(
#             "clients"
#         )  # Redirect to the client list or another appropriate page

#     services_with_totals = []
#     for service in client_services:
#         total_received = (
#             service.billing_set.aggregate(total=Sum("fees_recieved"))["total"] or 0
#         )
#         outstanding_amount = service.fee - total_received
#         services_with_totals.append(
#             {
#                 "service": service,
#                 "total_received": total_received,
#                 "outstanding_amount": outstanding_amount,
#             }
#         )

#     if request.method == "POST":
#         # Debug: Print the POST data received
#         print("Received POST data:")
#         print(f"Service IDs: {request.POST.getlist(f'service_id_{client.id}')}")
#         print(f"Payment Amounts: {request.POST.getlist(f'payment_amount_{client.id}')}")
#         print(f"Payment Type: {request.POST.get('payment_type')}")

#         service_ids = request.POST.getlist(f"service_id_{client.id}")
#         payment_amounts = request.POST.getlist(f"payment_amount_{client.id}")
#         payment_type = request.POST.get("payment_type")

#         # Check if the form is correctly submitted
#         if not service_ids or not payment_amounts or not payment_type:
#             messages.error(request, "Please fill out all fields.")
#             return redirect("generate_bill", pk=client.id)

#         for service_id, payment_amount in zip(service_ids, payment_amounts):
#             cservice = get_object_or_404(ClientService, id=service_id)
#             payment_amount = Decimal(payment_amount)
#             total_received = (
#                 cservice.billing_set.aggregate(total=Sum("fees_recieved"))["total"] or 0
#             )

#             # Debug: Print the total received before creating the billing entry
#             print(
#                 f"Total received for service {cservice.service.name}: {total_received}"
#             )

#             # Ensure the payment amount is positive
#             if payment_amount <= 0:
#                 messages.error(
#                     request,
#                     f"Invalid payment amount for service: {cservice.service.name}",
#                 )
#                 continue  # Skip this payment if it's invalid

#             # Create a new Billing record
#             print(
#                 f"Creating billing record for service {cservice.service.name} with payment amount: {payment_amount}"
#             )
#             total_received = Decimal(total_received)
#             Billing.objects.create(
#                 clientService=cservice,
#                 fees_recieved=Decimal(payment_amount),
#                 billing_date=now().date(),
#                 fee_status=(
#                     "Partial"
#                     if payment_amount + total_received < cservice.fee
#                     else "Paid"
#                 ),
#                 payment_type=payment_type,
#                 outstanding_amt=max(
#                     Decimal(0), cservice.fee - (payment_amount + total_received)
#                 ),
#             )

#         messages.success(request, "Payment successfully recorded!")
#         return redirect("generate_bill", pk=client.id)

#     context = {
#         "client": client,
#         "services_with_totals": services_with_totals,
#     }
#     return render(request, "generate_bill.html", context)


def generate_bill(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client_services = ClientService.objects.filter(client=client, status="Completed")

    # Check if there are any services for the client
    if not client_services:
        messages.error(request, "No completed services found for this client.")
        return redirect(
            "clients"
        )  # Redirect to the client list or another appropriate page

    services_with_totals = []
    for service in client_services:
        # Calculate the total received amount for the service
        total_received = (
            service.billing_set.aggregate(total=Sum("fees_recieved"))["total"] or 0
        )
        outstanding_amount = service.fee - Decimal(total_received)
        services_with_totals.append(
            {
                "service": service,
                "total_received": total_received,
                "outstanding_amount": outstanding_amount,
            }
        )

    if request.method == "POST":
        # Debug: Print the POST data received
        print("Received POST data:")
        print(f"Service IDs: {request.POST.getlist(f'service_id_{client.id}')}")
        print(f"Payment Amounts: {request.POST.getlist(f'payment_amount_{client.id}')}")
        print(f"Payment Type: {request.POST.get('payment_type')}")

        service_ids = request.POST.getlist(f"service_id_{client.id}")
        payment_amounts = request.POST.getlist(f"payment_amount_{client.id}")
        payment_type = request.POST.get("payment_type")

        # Check if the form is correctly submitted
        if not service_ids or not payment_amounts or not payment_type:
            messages.error(request, "Please fill out all fields.")
            return redirect("generate_bill", pk=client.id)

        for service_id, payment_amount in zip(service_ids, payment_amounts):
            cservice = get_object_or_404(ClientService, id=service_id)
            payment_amount = Decimal(payment_amount)

            # Calculate total received before making the payment entry
            total_received = (
                cservice.billing_set.aggregate(total=Sum("fees_recieved"))["total"] or 0
            )

            # Ensure the payment amount is positive
            if payment_amount <= 0:
                messages.error(
                    request,
                    f"Invalid payment amount for service: {cservice.service.name}",
                )
                continue  # Skip this payment if it's invalid

            # Create a new Billing record
            Billing.objects.create(
                clientService=cservice,
                fees_recieved=payment_amount,
                billing_date=now().date(),
                fee_status=(
                    "Partial"
                    if (payment_amount + total_received) < cservice.fee
                    else "Paid"
                ),
                payment_type=payment_type,
                outstanding_amt=max(
                    Decimal(0), cservice.fee - (payment_amount + total_received)
                ),
            )

        messages.success(request, "Payment successfully recorded!")
        return redirect("generate_bill", pk=client.id)

    context = {
        "client": client,
        "services_with_totals": services_with_totals,
    }
    return render(request, "generate_bill.html", context)


def send_payment_reminder_email(client, due_date):
    # Send reminder email to admin
    subject = f"Payment Reminder for {client.clientName}"
    message = f"Dear Sir, \n\nA partial payment was made by {client.clientName}. The remaining balance is due by {due_date}. \n\nPlease follow up with the client."
    admin_email = "haresh9771@gmail.com"  # Replace with actual admin email
    send_mail(subject, message, "no-reply@gmail.com", [admin_email])
