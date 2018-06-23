from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product

# Create your views here.

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
