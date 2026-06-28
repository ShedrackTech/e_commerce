# shop/urls.py
from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    PasswordChangeDoneView,
)
from . import views
app_name = 'shop'
urlpatterns = [
    path('', views.product_list, name='product_list'), 
    path('about/',   views.about,   name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),   
    path('register/',  views.register,           name='register'),
    path('login/',     views.ShopLoginView.as_view(),  name='login'),
    path('logout/',    views.ShopLogoutView.as_view(), name='logout'),
    path('profile/',   views.profile,            name='profile'),
    path('password-change/',
         views.ShopPasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/',
         PasswordChangeDoneView.as_view(
             template_name='shop/password_change_done.html'),
         name='password_change_done'),
    path('password-reset/',
         PasswordResetView.as_view(
             template_name='shop/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(
             template_name='shop/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='shop/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/',       PasswordResetCompleteView.as_view(
             template_name='shop/password_reset_complete.html'),
         name='password_reset_complete'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
   
]
    

