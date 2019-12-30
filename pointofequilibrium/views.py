import math
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, Http404, redirect
from django.http  import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib  import messages
from .models import ProductType, Product, Projection, ProjectionType, Duration, Bank,VariableEconomic
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
    duration = Duration.objects.all()
    print(object_user.id)
    print(duration )
    if user is not None:
        login(request, user)
        context = {
            "producttypes" : ProductType.objects.all(),
            "products" : Product.objects.all(),
            "object_user" : object_user,
            "duration": duration
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
    durations = Duration.objects.all()
    banks = Bank.objects.all()
    print(banks)
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
        "durations": durations,
        "banks": banks,

    }
    for i in durations:
        print(i)
    return render(request, "pointofequilibrium/productone.html", context)

def form_values_bank(request, product_id, user_id):
    duration = Duration.objects.all()
    banks = Bank.objects.all()
    product = Product.objects.get(pk=product_id)
    print(product)
    ted=0.0
    tem=0.0
    cuota=0.0
    fvp=0.0
    total=0.0
    cuotaOne=0.0
    list_coutas = []
    list_cuotasNumber = []
    row_data = []
    row_projection = []
    cuotaTwo=0.0
    try:
        if request.method == 'POST':
            
            duration = Duration.objects.all()
            object_user = User.objects.get(pk=user_id)
            object_user_id = object_user.id
            user_id = object_user_id
            print(object_user.id)
            #passenger_id = int(request.POST["passenger"])
            amount = int(request.POST["amount"])
            duration_id = int(request.POST["duration"])
            bank_id = request.POST["bank"]
            now = datetime.datetime.now()
            print(amount)
            print(duration_id)
            print(bank_id)
            print(now)
            product = Product.objects.get(pk=product_id)
            producType_id = product.productType.id

            object_projectionType = ProjectionType.objects.get(productType_id= producType_id)
            object_varibleOne = VariableEconomic.objects.get(bank_id=bank_id, duration_id=duration_id)
            object_duration = Duration.objects.get(id=duration_id)
            object_varible_id = object_varibleOne.id
        
            print(object_duration.limite_superior)
            months = int(object_duration.limite_superior/30)
            print(months)
            
            p = Projection(type_of_projection=object_projectionType, amount=amount,  date_modified=now, user=object_user, variableEconomic=object_varibleOne)
            p.save()
            
            if object_projectionType.name == 'Proyección credito de consumo':
                tem = math.pow(( 1 + object_varibleOne.value), 1/12) -1
                ted = math.pow(( 1 + tem), 1/30) -1
                b = 0.0
                cuota = 0.0
                fvp = 0.0
                row_data = []
                row_projection = []
                numerCuota = 0
                for i in range(months):
                    a  = i + 1 * 30
                    b  = b + a 
                    c = 1 / math.pow(( 1 + ted), a)
                    fvp = fvp + c
                    numberCuota = 1 + i
                    cuota = amount / fvp
                    cuotaOne = round(cuota, 3)
                    row_data.append(numberCuota)
                    row_data.append(cuotaOne)
                    row_projection.append(row_data)
                list_coutas = []
                cuotaTwo = round(cuota, 3)    
                total = 0.0
                total = cuota * months
            else:
                tem = math.pow(( 1 + object_varibleOne.value), 1/12) -1
                ted = math.pow(( 1 + tem), 1/30) -1
                b = 0.0
                cuota = 0.0
                fvp = 0.0
                row_data = []
                row_projection = []
                numerCuota = 0
                for i in range(months):
                    a  = i + 1 * 30
                    b  = b + a 
                    c = 1 / math.pow(( 1 + ted), a)
                    fvp = fvp + c

                    numberCuota = 1 + i
                    
                    cuota = amount / fvp
                    cuotaOne = round(cuota, 3)
                    row_data.append(numberCuota)
                    row_data.append(cuotaOne)
                    row_projection.append(row_data)
                list_coutas = []
                cuotaTwo = round(cuota, 3)    
                total = 0.0
                total = cuota * months
                total = total* 0.90

                context = {
        "p": p,
        "ted": ted,
        "tem": tem,
        "cuota": cuota,
        "months": months,
        "fvp" : fvp,
        "total": total,
        "object_user" : object_user,
        "user_id" : user_id,
        "list_coutas"  : list_coutas,
        "cuotaOne" : cuotaOne,
        "list_cuotasNumber" : list_cuotasNumber,
        "row_data ": row_data ,
        "row_projection": row_projection,
        "cuotaTwo": cuotaTwo,
        "amount":amount,

        
    }         
    

                return render(request, 'pointofequilibrium/cdt.html', context)


    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    context = {
        "p": p,
        "ted": ted,
        "tem": tem,
        "cuota": cuota,
        "months": months,
        "fvp" : fvp,
        "total": total,
        "object_user" : object_user,
        "user_id" : user_id,
        "list_coutas"  : list_coutas,
        "cuotaOne" : cuotaOne,
        "list_cuotasNumber" : list_cuotasNumber,
        "row_data ": row_data ,
        "row_projection": row_projection,
        "cuotaTwo": cuotaTwo,
        "amount":amount,

        
    }         
    
    return render(request, 'pointofequilibrium/projection.html', context)

def historial(request, user_id):
    object_user = User.objects.get(pk=user_id)
    user_id = object_user.id
    projections = Projection.objects.all().filter(user=user_id)
    print(object_user.id)
    print(projections)
    context = {
        "object_user": object_user,
        "projections": projections,


    }

    return render(request, 'pointofequilibrium/historial.html', context)

def checkNewTemplate(request):
    return render(request, 'pointofequilibrium/loginone.html')

