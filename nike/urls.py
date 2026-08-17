from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views

#app_name = 'nike'

urlpatterns = [
    path('', views.home, name='home'),
    path('nike1/', views.nike1, name='nike1'),
    path('signup/', views.signup, name='signup'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('register/', views.register, name='nike_register'),
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   #path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('add_blog_post/', views.add_blog_post, name='add_blog_post'),
    path('edit_blog_post/<int:post_id>/', views.edit_blog_post, name='edit_blog_post'),
    path('view_blog_post/', views.view_posts, name='view_posts'),
    path('delete_blog_post/<int:post_id>/', views.delete_blog_post, name='delete_blog_post'),
    path('basic_queries/', views.basic_queries, name='basic_queries'),
    path('aggregate_functions/', views.aggregate_functions, name='aggregate_functions'),
    path('f_expressions/', views.f_expressions, name='f_expressions'),
    path('raw_queries/', views.raw_queries, name='raw_queries'),
    path('relational_queries/', views.relational_queries, name='relational_queries'),
    path('custom_queries/', views.custom_queries, name='custom_queries'),
]