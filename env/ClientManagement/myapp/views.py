from django.shortcuts import render, redirect
from .models import Employee, Client

# Create your views here.
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
        clients = Client.objects.filter(employee=employee)  # Fetch clients assigned to the logged-in employee
        return render(request, "dashboard.html", {"clients": clients})
    except Employee.DoesNotExist:
        msg = "Employee not found."
        return render(request, "login.html", {"msg": msg})
    except Exception as e:
        print(e)
        msg = "Error fetching clients!!!"
        return render(request, "dashboard.html", {"clients": [], "msg": msg})
