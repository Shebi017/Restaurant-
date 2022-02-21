from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages
import json
from django.http import JsonResponse
# Create your views here.


def home(request):
    if request.user.is_anonymous:
        return redirect("/customer-login/")
    return render(request, 'home.html')

def product(request):
    if request.user.is_anonymous:
        return redirect("/customer-login/")
    q = request.GET.get('q')
    if q is not None:
        q = request.GET.get('q')
        items = Product.objects.filter(category=q)
    else:
        q = ""
        items = Product.objects.all()

    heading = ""
    if q=="":
        heading = "ALL FOOD"
    elif q=="V":
        heading = "VEGETABLE FOOD"
    else:
        heading = "NON VEGETABLE FOOD"

    customer=request.user.customer
    order = Order.objects.filter(customer=customer,complete=False).last()
    if order is None:
        order = {}
        
    context={
        'items':items,
        'heading':heading,
        'order':order,
    }
    return render(request, 'product.html',context)

def detail(request,pk):
    if request.user.is_anonymous:
        return redirect("/customer-login/")
    item = Product.objects.get(id=pk)
    context={
        'item':item,
    }
    return render(request, 'detail.html',context)

def cart(request):
    if request.user.is_anonymous:
        return redirect("/customer-login/")
    customer=request.user.customer
    order = Order.objects.filter(customer=customer,complete=False).last()
    if order is None:
        order = {}
        items = {}
    else:
        items = order.orderitem_set.all()
        print(f"ITEMS : {items} ")
    # branches = Branch.objects.all()
    context={
        'items':items,
        'order':order,
        # 'branches':branches,
 
    }
    return render(request, "cart.html",context)

def selectBranch(request):
    if request.user.is_anonymous:
        return redirect("/customer-login/")
    if request.method == "POST":
        branch_id = request.POST.get('branch_id')
        branch = Branch.objects.filter(id=branch_id).first()
        customer=request.user.customer
        order = Order.objects.filter(customer=customer,complete=False).last()
        if order is not None:
            order.branch = branch
            order.save()
            return redirect('/order/')
    
    branches = Branch.objects.all()

    context={
        'branches':branches,
    }

    return render(request, 'branch.html',context)
            


def updatecart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ####### Data From FrontEnd  ###########
        product_id = data.get('product_id')
        product = Product.objects.get(id=product_id)
        user = request.user
        customer,created = Customer.objects.get_or_create(user=user)       
        action = data.get('action')
        #######################################
        print(product_id)
        print(customer)
        print(created)
        print(action)
        ### Now Create or Get Order #######
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        print(order)
        print(created)
        orderitem,createditem = OrderItem.objects.get_or_create(order=order,product=product)
        if action=="add":
            orderitem.quantity = (orderitem.quantity +1)
        else:
            orderitem.quantity = (orderitem.quantity -1)
        orderitem.save()
        if orderitem.quantity <= 0:
            orderitem.delete()
        
        print(orderitem)
        print(createditem)
        # messages.success(request,"1 item is added into cart ")
        return JsonResponse("Data is received successfully",safe=False)

    return JsonResponse("Update Page !",safe=False)


def order(request):
    if request.user.is_anonymous:
        return redirect("/customer-login/")
    customer=request.user.customer
    order = Order.objects.filter(customer=customer,complete=False).last()
    if order is None:
        order = {}
    order.complete = True
    # order.branch =

    order.save()

    messages.success(request, "Order is Submitted successfully.")

    return redirect('/')


def customerLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        #  method to check user is valid or not
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            print('User is Login successfully...')
            messages.success(request, 'Customer is Login Successfull')
            return redirect('/')
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('/customer-login/')
    context={
        'role':'CUSTOMER',
    }
    return render(request, 'login.html',context)

def userRegister(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        user_check = User.objects.filter(username=username).first()

        email_check = User.objects.filter(email=email).first()

        if user_check is not None:
            messages.success(request,"Username is already taken.Please choose another name.")
            return redirect("/register/")

        if email_check is not None:
            messages.success(request,"Email is already taken. Pleese choose another email")
            return redirect("/register/")

        user = User(username=username,first_name=fname,last_name=lname,email=email)
        user.set_password(password)

        user.save()

        customer = Customer(user=user,address=address,contact_no=phone)

        customer.save()
        return redirect("/customer-login/")
    return render(request, 'register.html')


def getCheff(request):
    if request.method == "POST":
        order_id = request.POST.get('id')
        print('Order is made successfully ....',order_id)
        order = Order.objects.get(id=order_id)
        order.order_made = True
        order.save()

        messages.success(request, 'Order is made successfully ....')
        return redirect('/cheff/')
    cheff = Cheff.objects.filter(user=request.user).first()

    print(cheff)

    branch = Branch.objects.filter(cheff=cheff).first()

    print(branch)

    orders = Order.objects.filter(branch=branch,order_made=False)

    # print(order.customer.user.username)
    items = []
    for order in orders:
        items.append(order.orderitem_set.all())
        print(order)

    print(items)

    data = zip(orders,items)

    print(data)

    context={
        'data':data,
        'branch':branch,
    }

    return render(request, 'cheff.html',context)


def getWaiter(request):
    if request.method == "POST":
        order_id = request.POST.get('id')
        print('Order is picked successfully ....',order_id)
        order = Order.objects.get(id=order_id)
        order.order_pickup = True
        order.save()

        messages.success(request, 'Order is picked successfully ')
        return redirect('/waiter/')
    waiter = Waiter.objects.filter(user=request.user).first()

    print(waiter)

    branch = Branch.objects.filter(waiter=waiter).first()

    print(branch)

    orders = Order.objects.filter(branch=branch,order_pickup=False)

    # print(order.customer.user.username)
    items = []
    for order in orders:
        items.append(order.orderitem_set.all())
        print(order)

    print(items)

    data = zip(orders,items)

    print(data)

    context={
        'data':data,
        'branch':branch,
    }

    return render(request, 'waiter.html',context)
    
def getCashier(request):
    if request.method == "POST":
        order_id = request.POST.get('id')
        print('Payment is done ....',order_id)
        order = Order.objects.get(id=order_id)
        order.payment_done = True
        order.save()

        messages.success(request, 'Payment is done successfully')
        return redirect('/cashier/')
    cashier = Cashier.objects.filter(user=request.user).first()

    print(cashier)

    branch = Branch.objects.filter(cashier=cashier).first()

    print(branch)

    orders = Order.objects.filter(branch=branch,payment_done=False)

    # print(order.customer.user.username)
    items = []
    for order in orders:
        items.append(order.orderitem_set.all())
        print(order)

    print(items)

    data = zip(orders,items)

    print(data)

    context={
        'data':data,
        'branch':branch,
    }

    return render(request, 'cashier.html',context)
    
def cheffLogin(request):
    if request.method == "POST":
        print('############################')
        role = request.POST.get('role')
        print(role)
        print('############################')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            print('User is Login successfully...')
            cheff = Cheff.objects.filter(user=user).first()
            if cheff is None:
                messages.success(request,"Invalid Cheff username or password")
                return redirect('/cheff-login/')
            else:
                messages.success(request, "Cheff is Login Successfully")
                return redirect('/cheff/')
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('/cheff-login/')
    context={
        'role':'CHEFF',
    }
            
    return render(request, 'login.html',context)

def waiterLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            print('User is Login successfully...')
            waiter = Waiter.objects.filter(user=user).first()
            if waiter is None:
                messages.success(request,"Invalid Waiter username or password")
                print('Waiter name or pass is invalid')
                return redirect('/waiter-login/')
            else:
                messages.success(request, "Waiter is Login Successfully")
                return redirect('/waiter/')
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('/waiter-login/')
    context={
        'role':'WAITER',
    }
            
    return render(request, 'login.html',context)


def cashierLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            print('User is Login successfully...')
            cashier = Cashier.objects.filter(user=user).first()
            if cashier is None:
                messages.success(request,"Invalid Cashier username or password")
                return redirect('/cashier-login/')
            else:
                messages.success(request, "Cashier is Login Successfully")
                return redirect('/cashier/')
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('/cashier-login/')
    context={
        'role':'CASHIER',
    }
            
    return render(request, 'login.html',context)


def getManager(request):
    manager = Manager.objects.filter(user=request.user).first()

    print(manager)

    branch = Branch.objects.filter(manager=manager).first()

    cashier = Cashier.objects.filter(branch=branch)

    waiter = Waiter.objects.filter(branch=branch)

    cheff = Cheff.objects.filter(branch=branch)
    print(branch)

    orders = Order.objects.filter(branch=branch)

    # print(order.customer.user.username)
    items = []
    for order in orders:
        items.append(order.orderitem_set.all())
        print(order)

    print(items)

    data = zip(orders,items)

    print(data)

    context={
        'data':data,
        'branch':branch,
        'cashier':cashier,
        'waiter':waiter,
        'cheff':cheff,
    }

    return render(request, 'manager.html',context)



def managerLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            print('User is Login successfully...')
            manager = Manager.objects.filter(user=user).first()
            if manager is None:
                messages.success(request,"Invalid Manager username or password")
                return redirect('/manager-login/')
            else:
                messages.success(request, "Manager is Login Successfully")
                return redirect('/manager/')
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('/manager-login/')
    context={
        'role':'MANAGER',
    }
            
    return render(request, 'login.html',context)



def userLogout(request):
    logout(request)
    return redirect("/")