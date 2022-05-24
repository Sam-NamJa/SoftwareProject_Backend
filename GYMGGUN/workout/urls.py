from django.urls import path
from . import views


urlpatterns = [
    path('planSet', views.plan_set),
    path('planGet/<plan_name>', views.plan_get),
    path('planGet/<uid>/UID', views.plan_get_uid),
    path('planDel/<plan_name>', views.plan_del),
    path('planGetHashTag/<hashtag>', views.plan_get_hashtag),
    path('plan/like', views.like_plan),
    path('plan/download', views.download_plan),
    path('plan/download/<uid>/UID', views.download_plan_get),
    path('plan/comment', views.comment_plan),
    path('plan/comment/<plan_name>', views.comment_plan_get),
]
