from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
# Create your views here.
from addresses.models import Address
from addresses.forms import AddressForm
from accounts.models import GuestEmail
# def cart_create(user=None):
#     cart_obj = Cart.objects.create(user=None)
#     print('new cart created')
#     return cart_obj

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # products = cart_obj.products.all()
    
    # total = 0
    # for x in products:
    #     total += x.price
    # print(total)
    # cart_obj.total = total
    # cart_obj.save()


    # del request.session['cart_id']
    # request.session['cart_id'] = "12"
    # cart_id = request.session.get("cart_id", None)
    # # if cart_id is None: #and isinstance(cart_id, int):
    # #     cart_obj = cart_create()
    # #     # cart_obj = Cart.objects.create(user=None)
    # #     request.session['cart_id'] = cart_obj.id
    # #     # print(' New Cart created')
    # # else:
    # qs = Cart.objects.filter(id=cart_id)
    # if qs.count() == 1:
    #     print('cart ID exists')
    #     cart_obj = qs.first()
    #     if request.user.is_authenticated and cart_obj.user is None:
    #         cart_obj.user = request.user
    #         cart_obj.save()
    # else:
    #     # cart_obj = cart_create()
    #     cart_obj = Cart.objects.new(user=request.user)
    #     request.session['cart_id'] = cart_obj.id
    # print(cart_id)
    # cart_obj = Cart.objects.get(id=cart_id)
        
    # print(request.session) # on the request
    # print(dir(request.session))
    # request.session.set_expiry(300)
    # request.session.session_key
    # key = request.session.session_key
    # print(key)
   
    # request.session['user'] = request.user.username
    return render(request, "carts/home.html", {"cart": cart_obj})

def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("show message to user, product is gone")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj) # cart_obj.products.add(3)
        request.session['cart_items'] = cart_obj.products.count()
    # cart_obj.products.remove(obj)
    # return redirect(product_obj.get_absolute_url())
    return redirect("cart:home")



def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")        

    # user = request.user
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    # billing_profile = None

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    # guest_email_id = request.session.get('guest_email_id')
    # if user.is_authenticated:
    #     # logged user checkout remember payment stuff
    #     billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    # elif guest_email_id is not None:
    #     # guest user checkout auto reloads payment stuff
    #     guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
    #     billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    # else:
    #     pass
    
    # print(billing_profile)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:  
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        # shipping_address_qs = address_qs.filter(address_type='shipping')
        # billing_address_qs = address_qs.filter(address_type='billing')
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        # order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        # if order_qs.count() == 1:
        #     order_obj = order_qs.first()
        # else:
            # old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
            # if old_order_qs.exists():
            #     old_order_qs.update(active=False)
            # order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)

        # order_qs = Order.objects.filter(cart=cart_obj, active=True)
        # if order_qs.exists():
        #     order_qs.update(active=False)
        # else:
        #     order_obj= Order.objects.create(cart=cart_obj, billing_profile=billing_profile)
        
        
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect("cart:success")
        

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form":address_form,
        "address_qs":address_qs,
    }
    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})