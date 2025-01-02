"""
URL configuration for ClientManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add_service/", views.add_service, name="add_service"),
    path("view_service/", views.view_service, name="view_service"),
    path("delete_service/<int:pk>", views.delete_service, name="delete_service"),
    path("add_client/", views.add_client, name="add_client"),
    path("update_client/<int:pk>", views.update_client, name="update_client"),
    path("delete_client/<int:pk>", views.delete_client, name="delete_client"),
    path("clients/", views.clients, name="clients"),
    path(
        "add_clientservice/<int:pk>/", views.add_clientservice, name="add_clientservice"
    ),
    path(
        "update_clientservice/<int:pk>/",
        views.update_clientservice,
        name="update_clientservice",
    ),
    path(
        "delete_clientservice/<int:pk>/",
        views.delete_clientservice,
        name="delete_clientservice",
    ),
    path("view_client/<int:pk>/", views.view_client, name="view_client"),
    path("generate_bill/<int:pk>/", views.generate_bill, name="generate_bill"),
    path("print_bill/<int:pk>/", views.print_bill, name="print_bill"),
    path("billing_list/", views.billing_list, name="billing_list"),
]
