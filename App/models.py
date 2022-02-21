from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class Cashier(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Cheff(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Manager(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Waiter(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Branch(models.Model):
    name = models.CharField(max_length=50)
    waiter = models.OneToOneField(Waiter, on_delete=models.CASCADE)
    cheff = models.OneToOneField(Cheff, on_delete=models.CASCADE)
    cashier = models.OneToOneField(Cashier, on_delete=models.CASCADE)
    manager = models.OneToOneField(Manager, on_delete=models.CASCADE,default="")

    def __str__(self):
        return self.name
    



class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/upload/")
    price = models.FloatField(default=0.0)
    description = models.TextField()
    choices = [
        ('V','Vegetables'),
        ('NV','Non-Vegetables')
    ]
    category = models.CharField(max_length=20,choices=choices)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    order_pickup = models.BooleanField(default=False)
    order_made = models.BooleanField(default=False)
    payment_done = models.BooleanField(default=False)


    def __str__(self):
        return str(self.id)

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

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True,default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


