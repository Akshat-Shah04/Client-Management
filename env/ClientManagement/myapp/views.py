from django.shortcuts import render, redirect
from .models import Employee, Client, Service, ClientService, Payment
from django.contrib import messages

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

            # Get selected service IDs from the POST data
            service_ids = request.POST.getlist("services")
            for service_id in service_ids:
                service = Service.objects.get(id=service_id)
                ClientService.objects.create(
                    service=service,
                    client=client,
                    fee=0,  # Set fee to 0 or another default value
                )

            messages.success(request, "Client created successfully.")
            return redirect("dashboard")  # Redirect to the dashboard or another page

        except Exception as e:
            print(">" * 30, " Error Occurred >>>>> add_client >>>>>", e)
            messages.error(request, f"An error occurred: {e}")
            return render(
                request, "add_client.html", {"services": Service.objects.all()}
            )
    else:
        # Render the form with available services
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
