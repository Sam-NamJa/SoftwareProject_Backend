from django.urls import path, include
from userInfo import views

urlpatterns = [
    path('', views.info),
    # path('<int:pk>', views.info_detail)
]