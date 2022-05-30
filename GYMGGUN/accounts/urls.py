from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup),
    path('phone', views.phone),
    path('login', views.login),
    path('logout', views.logout),
    path('info', views.info)
]
