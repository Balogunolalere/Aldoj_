from django.urls import path
from . import views

urlpatterns = [
    path('properties/', views.PropertyListCreate.as_view(), name='property_list_create'),
    path('properties/<int:pk>/', views.PropertyDetail.as_view(), name='property_detail'),  # Add this URL pattern for the property detail view
    path('investments/', views.InvestmentListCreate.as_view(), name='investment_list_create'),
    path('investments/<int:pk>/', views.InvestmentDetail.as_view(), name='investment_detail'),  # Add this URL pattern for the investment detail view
    path('crops/', views.CropListCreate.as_view(), name='crop_list_create'),
    path('crops/<int:pk>/', views.CropDetail.as_view(), name='crop_detail'),  # Add this URL pattern for the crop detail view
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register-admin/', views.AdminRegisterView.as_view(), name='register_admin'),
]
