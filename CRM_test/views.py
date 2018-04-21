from django.shortcuts import render

from CRM_test.models import UserProfile

# Create your views here.


def index(request):

    return render(request, "index.html")


def customer_list(request):

    return render(request, "sales/customers.html")