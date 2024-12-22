from django.shortcuts import render, redirect
from .models import Employee, Client, Service, ClientService, Payment
from django.contrib import messages

# Create your views here.


def signup(request):
    if request.method == "POST":
        emp_name = request.POST.get("emp_name")
        salary = request.POST.get("salary")
        emp_aadhar = request.POST.get("emp_aadhar", "NA")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        status = "Active"
        password = request.POST.get("password")

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
        # For GET requests, render the login page
        return render(request, "login.html")


def logout(request):
    # Clear session data
    request.session.flush()
    return redirect("login")  # Use named route if configured in urls.py


def dashboard(request):
    try:
        employee = Employee.objects.get(email=request.session["email"])
        clients = Client.objects.filter(
            employee=employee
        )  # Fetch clients assigned to the logged-in employee
        return render(request, "dashboard.html", {"clients": clients})
    except Employee.DoesNotExist:
        msg = "Employee not found."
        return render(request, "login.html", {"msg": msg})
    except Exception as e:
        print(e)
        msg = "Error fetching clients!!!"
        return render(request, "dashboard.html", {"clients": [], "msg": msg})


def create_client(request):
    if request.method == "POST":
        try:
            # Fetch the logged-in employee
            employee = Employee.objects.get(email=request.session["email"])

            # Get referredBy (optional)
            referred_by_id = request.POST.get("referredBy", None)
            referred_by = (
                Client.objects.get(id=referred_by_id) if referred_by_id else None
            )

            # Create the client
            client = Client.objects.create(
                clientName=request.POST["clientName"],
                employee=employee,
                status="Active",  # Default status
                pan=request.POST["pan"],
                city=request.POST["city"],
                aadhar=request.POST["aadhar"],
                mobile=request.POST["mobile"],
                email=request.POST["email"],
                referredBy=referred_by,
            )

            # Add services
            service_ids = request.POST.getlist("services")  # List of service IDs
            for service_id in service_ids:
                service = Service.objects.get(id=service_id)
                # Create a ClientService instance linking the client to the service
                clientServ = ClientService.objects.create(
                    client=client,
                    service=service,
                    fee=0,  # No fee set initially; can be updated when billing
                )
                print(30 * ">", "Client Service => >>>>>", clientServ)

            messages.success(request, "Client created successfully!")
            return redirect("dashboard")  # Redirect to the dashboard or desired page

        except Employee.DoesNotExist:
            messages.error(request, "Logged-in employee not found.")
            return redirect("login")
        except Service.DoesNotExist:
            messages.error(request, "Selected service not found.")
        except Exception as e:
            messages.error(request, f"Error creating client: {e}")

    # For GET requests, render the create client page with required data
    employees = Employee.objects.all()
    services = Service.objects.all()
    clients = Client.objects.all()
    return render(
        request,
        "create_client.html",
        {
            "employees": employees,
            "services": services,
            "clients": clients,
        },
    )
