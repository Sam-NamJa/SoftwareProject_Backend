from django.urls import path
from . import views

urlpatterns = [
    path('planSet', views.plan_set),
    path('planGet/<plan_name>', views.plan_get),
    path('planGetUID/<uid>', views.plan_get_uid),
    path('planGetHashTag/<hashtag>', views.plan_get_hashtag),
]