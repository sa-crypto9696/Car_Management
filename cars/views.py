
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Car
from .forms import CarForm
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView



@login_required
def car_list(request):
    cars = Car.objects.filter(user=request.user)
    return render(request, 'car_list.html', {'cars': cars})

@login_required
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id, user=request.user)
    return render(request, 'car_detail.html', {'car': car})

@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            car.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})

@login_required
def update_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, user=request.user)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = CarForm(instance=car)
    return render(request, 'update_car.html', {'form': form})

@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, user=request.user)
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')
    return render(request, 'delete_car.html', {'car': car})

@login_required
def search_cars(request):
    query = request.GET.get('q')
    if query:
        cars = Car.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query),
            user=request.user
        )
    else:
        cars = Car.objects.none()
    return render(request, 'search_results.html', {'cars': cars})


def custom_login(request):
    if request.method == 'POST':
        # If it's a login attempt
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('car_list')  # Redirect to a car list page after successful login
            else:
                return render(request, 'registration/login.html', {'error': 'Invalid credentials.'})
        
        # If it's a registration attempt
        elif 'register' in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                login(request, new_user)
                return redirect('car_list')  # Redirect to car list after successful registration
            else:
                return render(request, 'registration/login.html', {'form': form, 'error': 'Registration failed.'})
    else:
        form = UserCreationForm()
    return render(request, 'registration/login.html', {'form': form})