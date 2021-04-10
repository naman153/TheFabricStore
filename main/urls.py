from django.contrib import auth
from django.urls import path
from main import views
from main.views import product_detail

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('about-us/', views.about_us, name="about-us"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('product_detail/<int:pk>/<slug:slug>/', views.product_detail, name="product_detail"),
	path('signup/',views.account ,name='account'),
	path('login/',views.login , name='login'),
	path('logout/',views.logout,name='logout'),
	path('contact_us/', views.contact_us, name='contact_us'),
	path('feedback/' ,views.feedback, name='feedback'),
	path('product/<slug:slug>/' , views.product, name='product'),
	path('success/<int:pk>/', views.success, name='success'),


]