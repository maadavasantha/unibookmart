from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add/', views.book_create, name='book_create'),
    path('edit/<int:pk>/', views.book_update, name='book_update'),
    path('delete/<int:pk>/', views.book_delete, name='book_delete'),
]