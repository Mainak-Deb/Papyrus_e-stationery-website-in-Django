from django.shortcuts import render,redirect,HttpResponse
from .models import Product, Contact,Orders,OrderUpdate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login, logout 

from django.contrib import messages
from django.utils import timezone
from math import ceil
# import the logging library
import logging
import json


# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.
from django.http import HttpResponse

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds}
    return render(request, 'index.html', params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<3:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'search.html', params)



def about(request):
    
    return render(request,"about.html")
    #return HttpResponse("we are in home")



@login_required(login_url='handleLogin')
def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '') 
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        total= request.POST.get('total', '')
        username= request.POST.get('username', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone,total=total)
        order.save()
        orderupdate=OrderUpdate(name=username,items_json=items_json,timestamp=timezone.now())
        orderupdate.save()
        thank = True
        id = order.order_id
        return render(request, 'checkout.html', {'thank':thank, 'id': id})
    
    return render(request, 'checkout.html')


def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        msg = request.POST.get('msg', '')
        contact = Contact(name=name, email=email, phone=phone, msg=msg)
        contact.save()
    
    return render(request, 'contact.html')


def productView(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, "product_page.html", {'product':product[0]})


def catagory(request, cats):

  
    query = cats
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<3:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, "catagory.html", params)

def sales(request):
    allProds = []
    saleprods = Product.objects.values('sale', 'id')
    sales = {item['sale'] for item in saleprods}
    for sale in sales:
        prod = Product.objects.filter(sale=sale)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds}
    return render(request, 'sales.html', params)





def handleSignup(request):
	if request.method== "POST":
		#Get the post parameters
		username =request.POST['username']
		fname =request.POST['fname']
		lname =request.POST['lname']
		email =request.POST['email']
		pass1 =request.POST['pass1']
		pass2 =request.POST['pass2']
		address =request.POST['address']

		#checks for erroneous inputs

		if (len(username)>10) :
			messages.error(request,"username must be under 10 characters")
			return redirect("home")
        
		#create the user
		if (pass1!=pass2) :
			messages.error(request,"password do not match")
			return redirect("home")
        
		#create the user        
		

		myuser= User.objects.create_user(username,email,pass1)
		myuser.first_name =fname
		myuser.last_name =lname
		myuser.save()
		messages.success(request,"Your Papyrus Account Has Been Succesfully Created, Please Login To Continue")
		return redirect("home")

	else:
		return HttpResponse('404 - Not Found')


def handleLogin(request):
	if request.method== "POST":
		#Get the post parameters
		loginusername =request.POST['loginusername']
		loginpassword =request.POST['loginpassword']	


		user =auth.authenticate(username=loginusername,password=loginpassword)

		if user is not None:
			auth.login(request,user)
			messages.success(request,"Succesfully logged In")
			return redirect("home")

		else:
			messages.error(request,"Invalid Credentials")
			return redirect("home")

	messages.error(request,"Please Signup Or Login to Continue")
	return redirect("home")


def handleLogout(request):
		logout(request)
		messages.success(request,"Succesfully logged Out")
		return redirect("home")


def tracker(request):
    name = request.GET.get('usertracker')
    # updates=[]
    update = OrderUpdate.objects.filter(name=name)
    # updates.append({'text': item.update_desc, 'time': item.timestamp,'Orders': item.items_json})
   
    
    update = OrderUpdate.objects.filter(name=name)
    print(update)
    if len(update)>0:
        updates = []
        for item in update:
            print(item.timestamp)
            jd=json.loads(item.items_json)
            jl=[]
            for i in jd:  
                    jl.append(jd[i])
                
            updates.append([ item.update_desc, item.timestamp, jl])
            # print(item.update_desc, item.timestamp,item.items_json)
            
        params = {'updates':updates}
        # return HttpResponse(updates)
    else:
        return HttpResponse('{"status":"noitem"}')
    return render(request, 'tracker.html',params)
