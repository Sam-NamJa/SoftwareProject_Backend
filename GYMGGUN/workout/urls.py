from django.urls import path
from . import views

urlpatterns = [
    path('planSet', views.plan_set),
    path('planGet', views.plan_get),
]