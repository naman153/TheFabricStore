from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.base import Model

class Enquiry(models.Model):
	name = models.CharField(max_length=50, null=False)
	phone = models.CharField(max_length=12, null=False, blank=False, unique=True)
	email= models.CharField(max_length=100, null=True)
	message= models.CharField(max_length=250, null=False)


class Feedback(models.Model):
	image = models.ImageField(null=True)
	name = models.CharField(max_length=50, null=False)
	star = models.IntegerField(null=False)
	message= models.CharField(max_length=250, null=False)

	@property
	def starr(self):
		star= self.star
		return ("1" * star)

	@property
	def unstar(self):
		star = self.star
		unstar= 5 - star
		return ("1" * unstar)

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	

	def __str__(self):
		return self.name

category_choices=(
		('cotton', 'COTTON'),
		('jute', 'JUTE'),
		('viscose', 'VISCOSE'),
		('cotrey', 'COTREY'),
		('linen', 'LINEN'),
		('silk','SILK'),
	)

class Product(models.Model):

	
	category= models.CharField(max_length=15 ,choices=category_choices, default="cotton")
	name = models.CharField(max_length=200)
	color = models.CharField(max_length=200, null=False, default="White")
	width = models.FloatField(default=False)
	price = models.FloatField()
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url



class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = True
		orderitems = self.orderitem_set.all()
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

	@property
	def get_tax(self):
		orderitems = self.orderitem_set.all()
		subtotal = sum([item.get_total for item in orderitems])
		total=(subtotal * 0.18)
		return total 

	@property
	def get_total(self):
		orderitems = self.orderitem_set.all()
		subtotal = sum([item.get_total for item in orderitems])
		total=subtotal + (subtotal * 0.18)
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	product_quantity= models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.product_quantity
		return total
	
	


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address