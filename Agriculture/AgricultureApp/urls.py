from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('AdminLogin.html', views.AdminLogin, name="AdminLogin"), 
	       path('AdminLoginAction', views.AdminLoginAction, name="AdminLoginAction"),
	       path('FarmerLogin.html', views.FarmerLogin, name="FarmerLogin"), 
	       path('FarmerLoginAction', views.FarmerLoginAction, name="FarmerLoginAction"),
	       path('ConsumerLogin.html', views.ConsumerLogin, name="ConsumerLogin"), 
	       path('ConsumerLoginAction', views.ConsumerLoginAction, name="ConsumerLoginAction"),
	       path('Register.html', views.Register, name="Register"),
	       path('Signup', views.Signup, name="Signup"),
	       path('AddProduct.html', views.AddProduct, name="AddProduct"),
	       path('AddProductAction', views.AddProductAction, name="AddProductAction"),
	       path('UpdateProduct', views.UpdateProduct, name="UpdateProduct"),
	       path('UpdateQuantity', views.UpdateQuantity, name="UpdateQuantity"),
	       path('UpdateQuantityAction', views.UpdateQuantityAction, name="UpdateQuantityAction"),
	       path('ViewSales', views.ViewSales, name="ViewSales"),
	       path('ViewFarmerSales', views.ViewFarmerSales, name="ViewFarmerSales"),
	       path('AddFarmerProduct.html', views.AddFarmerProduct, name="AddFarmerProduct"),
	       path('AddFarmerProductAction', views.AddFarmerProductAction, name="AddFarmerProductAction"),
	       path('UpdateFarmerProduct', views.UpdateFarmerProduct, name="UpdateFarmerProduct"),
	       path('UpdateFarmerQuantity', views.UpdateFarmerQuantity, name="UpdateFarmerQuantity"),
	       path('UpdateFarmerQuantityAction', views.UpdateFarmerQuantityAction, name="UpdateFarmerQuantityAction"),
	       path('Purchase', views.Purchase, name="Purchase"),
	       path('PurchaseAction', views.PurchaseAction, name="PurchaseAction"),
	       path('SavePurchase', views.SavePurchase, name="SavePurchase"),
]