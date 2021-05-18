from django.contrib import auth
from django.contrib.auth import logout
from django.forms.forms import Form
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, request
import json
import datetime
from .models import * 

from .utils import cookieCart, cartData, guestOrder



def store(request):
	
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	feeds = Feedback.objects.all()
	products = Product.objects.all()
	
	context = {'products':products, 'cartItems':cartItems, 'feeds':feeds}
	return render(request, 'main/main.html', context)


def feedback(request):
	data = cartData(request)
	cartItems = data['cartItems']

	if request.method == "POST":
		name=request.POST['name']
		star=request.POST['star']
		image=request.POST['images']
		message=request.POST['message']
		x= Feedback.objects.create(name=name, image=image, star=star , message=message)
		x.save()
		return redirect('/')

	context={'cartItems':cartItems}
	return render(request, 'main/feedback.html',context)

		

def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']


	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'main/cart.html', context)


def about_us(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'main/about-us.html', context)

		
def logout(request):
	auth.logout(request)
	return redirect('/')


def product_detail(request,pk,slug):
	data= cartData(request)
	allproducts=Product.objects.all()
	cartItems = data['cartItems']
	order = data['order']
	product=Product.objects.get(id = pk)
	context={'product': product,'order':order,'cartItems':cartItems,'allproducts':allproducts}
	return render(request, 'main/product_detail.html',context)


def product(request, slug):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	feeds = Feedback.objects.all()
	if(slug != '\o'):
		products = Product.objects.filter(category = slug)
	else:
		products = Product.objects.all()

	
	context = {'products':products, 'cartItems':cartItems, 'feeds':feeds}
	return render(request, 'main/products.html', context)


def login(request):
	if request.method == "POST":
		username1 = request.POST['username']
		password1 = request.POST['password']
		x=auth.authenticate(username=username1, password=password1)
		if x is None:
			return redirect('login/')

		
		else:
			auth.login(request,x)
			return redirect('/')

	return render(request,'main/login.html')

def contact_us(request):
	data = cartData(request)
	cartItems = data['cartItems']
	
	if request.method=="POST":
		name=request.POST['name']
		email_address=request.POST['email_address']
		phone=request.POST['phone']
		message=request.POST['message']
		x= Enquiry.objects.create(name=name, phone=phone, email=email_address , message=message)
		x.save()
		return redirect('/')

	context={'cartItems':cartItems}
	return render(request, 'main/contact_us.html',context)

def account(request):
	if request.method=="POST":
		username=request.POST['username']
		password=request.POST['password']
		first_name=request.POST['first_name']
		last_name=request.POST['last_name']
		email_address=request.POST['email_address']
		
		x=User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email_address)
		x.save()
		print("User Created")
		return redirect('/')

	return render(request,'main/account.html')

def success(request, pk):
	data = cartData(request)
	order = data['order']
	orderid = Order.objects.get(id = pk)

	context = {'orderid':orderid}
	return render(request, 'main/success.html', context)


def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'main/checkout.html', context)



def updateItem(request):
	data = json.loads(request.body)
	p_quantity = data['p_quantity']
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)
	print('p_quantity:',p_quantity)
	

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, product_quantity=p_quantity)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
		
		
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	
 
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)




def processOrder(request):
	data= cartData(request)
	order = data['order']

	transaction_id= datetime.datetime.now().timestamp()

	data = json.loads(request.body)
     
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total= float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_total:
			order.complete = True
			order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer = customer,
				order = order,
				address = data['shipping']['address'],
				city = data['shipping']['city'],
				state = data['shipping']['state'],
				zipcode = data['shipping']['zipcode'],
			)
     
	else:
		print("User is not logged in...")
	
	return JsonResponse('Payment Submitted..', safe=False)