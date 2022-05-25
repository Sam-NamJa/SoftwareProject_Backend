from django.urls import path
from . import views

urlpatterns = [
    path('get_profile/<UID>', views.get_profile),
    path('modify_profile/<UID>', views.modify_profile),
    path('get_portfolio/<uid>', views.get_portfolios),
    path('makes_portfolios/', views.makes_portfolios),
    path('modify_portfolio/<postN>', views.modify_portfolios),
    path('delete_portfolio/<postN>', views.delete_portfolios),
    path('post_comments/', views.post_comments),
    path('get_comments/<postN>', views.get_comments),
    path('delete_comments/<commentN>', views.delete_comments),
    path('get_click_portfoilo/<postN>', views.get_click_portfoilo),
    path('subscribe', views.subscribe_profile),
    path('portfolio', views.like_portfolio),
    path('subscribe/portfolio/<uid>', views.subscribe_tab),
    path('post_image/', views.post_image)
]
