from django.urls import path
from . import views
from .views import custom_login
from django.http import HttpResponseRedirect


urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('accounts/login/', custom_login, name='login'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('add/', views.add_car, name='add_car'),
    path('car/<int:car_id>/update/', views.update_car, name='update_car'),
    path('car/<int:car_id>/delete/', views.delete_car, name='delete_car'),
    path('search/', views.search_cars, name='search_cars'),
    # Route for API documentation using Postman
    path('api/docs/', lambda request: HttpResponseRedirect('https://your-postman-doc-url.com')),
]
