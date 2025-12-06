from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('request/create/', views.request_create, name='request_create'),
    path('request/<uuid:pk>/delete/', views.request_delete, name='request_delete'),
    path('request/<uuid:pk>/', views.request_detail, name='request_detail'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/request/<uuid:pk>/update/', views.admin_update_status, name='admin_update_status'),
]