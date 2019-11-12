from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, Http404, redirect
from django.http  import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib  import messages
from .models import ProductType, Product, Projection, ProjectionType
from django import forms
import datetime
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "pointofequilibrium/login.html", {"message": "Go in"})
    context = {
        "user" : request.user
    }
    return render(request, "pointofequilibrium/user.html", context)


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    object_user = User.objects.get(username= user)
    print(object_user.id)
    if user is not None:
        login(request, user)
        context = {
            "producttypes" : ProductType.objects.all(),
            "products" : Product.objects.all(),
            "object_user" : object_user
        }
        return render(request, 'pointofequilibrium/user.html', context)
    else:
        return render(request, "pointofequilibrium/login.html", {"message":"Invalid credencials, you need to register"})

def admin_view(request):

    return super(MyAdmin, self).response_change(request, obj)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('index')

    else:
        f = CustomUserCreationForm()

    return render(request, 'pointofequilibrium/register.html', {'form': f})

def product_choose(request, product_id, user_id):
    try:
        object_user = User.objects.get(pk=user_id)
        print(object_user.id)
        product = Product.objects.get(pk=product_id)
        producType_id = product.productType.id
        object_projectionType = ProjectionType.objects.get(productType_id= producType_id)
        object_projectiontype_id = object_projectionType.id
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    context ={
        "product": product,

    }
    return render(request, "pointofequilibrium/product.html", context)

def form_values_bank(request, product_id, user_id ):
    try:
        if request.method == 'POST':
            object_user = User.objects.get(pk=user_id)
            object_user_id = object_user.id
            print(object_user.id)
            amount = request.POST["amount"]
            duration = request.POST["duration"]
            interest_rate = request.POST["interest"]
            now = datetime.datetime.now()
            print(now)
            product = Product.objects.get(pk=product_id)
            producType_id = product.productType.id
            object_projectionType = ProjectionType.objects.get(productType_id= producType_id)
            object_projectiontype_id = object_projectionType.id
            p = Projection(type_of_projection=object_projectionType, amount=amount,duration=duration, interest=interest_rate, date_modified=now, user=object_user )
            p.save()
            #context = {
                #"product" : Product.objects.get(pk=product_id),
                #"producType_id" : product.productType.id,
                #"object_projectionType" : ProjectionType.objects.get(productType_id= producType_id),
                #"object_projectiontype_id" : object_projectionType.id
            #}

    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    context = {
        "object_projectionType" : object_projectionType,
        "p": p
    }         

    return render(request, 'pointofequilibrium/projection.html', context)