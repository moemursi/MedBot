from django.shortcuts import render, redirect
from .models import Inventory, Customer, Admin, Employee, Cart
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate

def home(request):
	obj = Inventory.objects.all()
	context = {'all': obj}
	return render(request, 'home.html', context)

def about(request):
	return render(request, 'about.html', {})

def customerPortal(request):
	obj = Inventory.objects.all()
	context = {'all': obj}
	return render(request, 'customer.html', context)

def loginC(request):
	if request.session.is_empty():
		return render(request, 'loginportal.html', {})
	else:
		return redirect('customerx')


def loginCustomer(request):
	obj = Inventory.objects.all()
	context = {'all': obj}
	if request.method == "POST":
		username = request.POST['email']
		password = request.POST['password']
		if Customer.objects.filter(customer_email = username).exists():
			userX = Customer.objects.get(customer_email = username)
			if password == userX.customer_password:
				request.session['userId'] = userX.customer_id
				request.session.set_expiry(300)
				return render(request, 'customer.html', context)
			else:
				return HttpResponse("invalid password")
		elif Employee.objects.filter(employee_email = username).exists():
			userE = Employee.objects.get(employee_email = username)
			if password == userE.employee_password:
				request.session['userId'] = userE.pharmacy_id
				request.session.set_expiry(300)
				response = redirect('pharmacypage')
				return response
			else:
				return HttpResponse("invalid password")
		elif Admin.objects.filter(admin_email = username).exists():
			userA = Admin.objects.get(admin_email = username)
			if password == userA.admin_password:
				request.session['userId'] = userA.admin_id
				request.session.set_expiry(300)
				response = redirect('adminpage')
				return response
			else:
				return HttpResponse("invalid password")
		else:
			return HttpResponse("invalid email")
	else:
		if request.session.is_empty():
			response = redirect('loginC')
			return response
		elif request.session['userId']:
			return render(request, 'customer.html', context)
		else:
			request.session.set_test_cookie()
			response = redirect('loginC')
			return response

def loginE(request):
	return render(request, 'employee.html', {})

def loginA(request):
	return render(request, 'admin.html', {})

def logoutC(request):
	try:
		request.session.flush()
	except KeyError:
		pass
	return HttpResponse("Logged out")

def registerC(request):
	if request.method == "POST":
		obj = Inventory.objects.all()
		context = {'all': obj}
		customerName = request.POST['username']
		customerEmail = request.POST['email']
		customerPassword = request.POST['password']
		customerAddress = request.POST['address']
		customerPhone = request.POST['phone']
		customerYear = request.POST['year']
		customerMonth = request.POST['month']
		customerDay = request.POST['day']
		objX = Customer(customer_name = customerName, birthdate = ''+customerYear+'-'+customerMonth+'-'+customerDay+'', customer_address = customerAddress, customer_password = customerPassword, customer_email = customerEmail, customer_phone = customerPhone)
		objX.save()
		response = redirect('loginC')
		return response
	else:
		return render(request, 'register.html', {})

def createUser(request):
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		address = request.POST['address']
		return HttpResponse("ok")

def settingsC(request):
	return render(request, 'settingsC.html', {})

def add_cart(request, list_id):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		obj = Inventory.objects.get(med_id = list_id)
		objC = Cart(pharmacy_id = obj.pharmacy_id, customer_id =  Customer.objects.get(customer_id = request.session['userId']), adding_quantity = 5, med_id = obj)
		objC.save()
		messages.success(request, ('Item added to the cart'))
		return redirect('home')

def cart(request):
	if request.session.is_empty():
		return redirect('loginC')
	else:
		obj = Cart.objects.filter(customer_id = request.session['userId'])
		context = {'all': obj}
		return render(request, 'cart.html', context)