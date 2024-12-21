from django.shortcuts import render, redirect
from .models import Employee, Client
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

            # Create a new employee
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
