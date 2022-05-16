from django.urls import path
from . import views

urlpatterns = [
    path('planSet', views.planSet),
]