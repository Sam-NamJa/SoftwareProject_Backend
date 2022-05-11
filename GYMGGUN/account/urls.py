from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('phone/', views.phone),
    path('signup/', views.signup)
]