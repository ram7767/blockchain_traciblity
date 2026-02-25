"""AgricultureApp URL Configuration — App-level routes."""

from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Admin
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/add-user/', views.admin_add_user, name='admin_add_user'),
    path('admin-panel/toggle-user/<int:user_id>/', views.admin_toggle_user, name='admin_toggle_user'),
    path('admin-panel/delete-user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    path('admin-panel/sales/', views.admin_view_sales, name='admin_view_sales'),

    # Farmer
    path('farmer/', views.farmer_dashboard, name='farmer_dashboard'),
    path('farmer/add-product/', views.farmer_add_product, name='farmer_add_product'),
    path('farmer/update-product/<int:product_id>/', views.farmer_update_product, name='farmer_update_product'),
    path('farmer/sales/', views.farmer_view_sales, name='farmer_view_sales'),

    # Consumer
    path('consumer/', views.consumer_dashboard, name='consumer_dashboard'),
    path('consumer/purchase/<int:product_id>/', views.consumer_purchase, name='consumer_purchase'),
]