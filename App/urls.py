from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('product/',views.product,name="product"),
    path('detail/<str:pk>/',views.detail,name="detail"),
    path('cart/',views.cart,name="cart"),
    path('update/',views.updatecart,name="update"),
    path('order/',views.order,name="order"),
    path('customer-login/',views.customerLogin,name="customer-login"),
    path('logout/',views.userLogout,name="logout"),
    path('register/',views.userRegister,name="register"),
    path('cheff/',views.getCheff,name="cheff"),
    path('cheff-login/',views.cheffLogin,name="cheff-login"),
    path('waiter/',views.getWaiter,name="waiter"),
    path('waiter-login/',views.waiterLogin,name="waiter-login"),
    path('cashier/',views.getCashier,name="cashier"),
    path('cashier-login/',views.cashierLogin,name="cashier-login"),
    path('manager-login/',views.managerLogin,name="manager-login"),
    path('manager/',views.getManager,name="manager"),
    path('select-branch/',views.selectBranch,name="select-branch"),
]