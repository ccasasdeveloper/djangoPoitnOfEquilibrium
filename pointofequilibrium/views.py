from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, Http404, redirect
from django.http  import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib  import messages
from .models import ProductType, Product
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
    if user is not None:
        login(request, user)
        context = {
            "producttypes" : ProductType.objects.all(),
            "products" : Product.objects.all()
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

def product_choose(request):
    try:
        product_id = request.POST['product']
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    context ={
        "product": product,

    }
    return render(request, "pointofequilibrium/product.html", context)


