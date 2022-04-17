from urllib import response
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from .models import Customer, Product, Cart, OrderPlaced, Order
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from app import forms


class ProductView(View):
    def get(self, request):
        totalitem = 0

        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')

        cooking_essentials = Product.objects.filter(category='CS')
        general_groceries = Product.objects.filter(category='GG')
        personal_care = Product.objects.filter(category='PC')
        cleaning_utility = Product.objects.filter(category='CU')
        beverages = Product.objects.filter(category='B')

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles,
                                                 'cooking_essentials': cooking_essentials,
                                                 'general_groceries': general_groceries,
                                                 'personal_care': personal_care, 'cleaning_utility': cleaning_utility,
                                                 'beverages': beverages,
                                                 'totalitem': totalitem})


class ProductDetailsView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request, 'app/productdetail.html', {'product': product, 'totalitem': totalitem})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')




# class Cart(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
#     item = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     purchased = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f'{self.quantity} X {self.item}'

#     def get_total(self):
#         total = self.item.price * self.quantity
#         float_total = format(total, '0.2f')
#         return float_total


# class Order(models.Model):
#     orderitems = models.ManyToManyField(Cart)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     ordered = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#     paymentId = models.CharField(max_length=264, blank=True, null=True)
#     orderId = models.CharField(max_length=200, blank=True, null=True)


#     def get_totals(self):
#         total = 0
#         for order_item in self.orderitems.all():
#             total += float(order_item.get_total())
#         return total

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 20.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.qunatity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount

            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount})
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
         
        
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))        
        c.qunatity += 1
       

        print('=====CCCC====', c)
        
        c.save()
        amount = 0.0
        shipping_amount = 20.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.qunatity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.qunatity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
    


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.qunatity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 20.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.qunatity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.qunatity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 20.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.qunatity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.qunatity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


# def profile(request):
#  return render(request, 'app/profile.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            Zipcode = form.cleaned_data['Zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, Zipcode=Zipcode)
            reg.save()
            return redirect('/checkout/')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add})


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation !! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 20.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.qunatity * p.product.discounted_price)
            amount += tempamount

        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    
    odr = Order()
    odr.user = user
    odr.save()
    sum_subtotal = 0
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, qunatity=c.qunatity, order=odr).save()
        # sum_subtotal += max((c.qunatity * c.product.selling_price)-(c.qunatity*c.product.discounted_price),0)
        tt = c.qunatity * c.product.selling_price
        sum_subtotal += max(tt,0)
        c.delete()
    odr.shipping_cost = 20
    odr.total = sum_subtotal
    odr.save()
    
    return redirect("confirm_order")


def confirm_order(request):
    user = request.user
    print('====User====: ', user)
    odr = Order.objects.filter(user=user).last()
    customer_data = Customer.objects.filter(user=user)
    # product_obj = OrderPlaced.objects.filter(user=user)
    product_obj = OrderPlaced.objects.filter(order=odr)
    # product_obj = odr.order_items
    

    context = {
        'user': user,
        'customer_data': customer_data,
        'product_obj': product_obj,
        'order': odr
    }
    return render(request, 'app/order_confirm.html', context)


def invoice_render_pdf(request, *args, **kwargs):
    pk = kwargs.get('pk') - 1
    odr = kwargs.get('odr')
    order = Order.objects.get(id=odr)
    print('====PK=====', pk)
    customer_data = Customer.objects.filter(user=pk)

    invoice = get_object_or_404(Customer, pk=pk)
    ord = get_object_or_404(OrderPlaced, pk=pk)
    print('========Orderd User', ord)
    # product_obj = OrderPlaced.objects.filter(pk=pk)
    product_obj = OrderPlaced.objects.filter(order=odr)
    last_order = OrderPlaced.objects.latest('ordered_date')
    last_order_item = OrderPlaced.objects.all().order_by('-id')[:3]
    
    # total = (item + item.total_cost for item in last_order_item())
    
    # return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    # print ('===Total===', total ) 
    
    
        
    # total_cost = 
    
    
    print('=======Last Order Item=====', last_order_item)
    print('=======Last Order=====', last_order)
    template_path = 'app/pdf.html'
    tmat = order.total + order.shipping_cost
    context = {
        'invoice': invoice,
        'product_obj': product_obj,
        'customer_datas': customer_data,
        'last_order': last_order,
        'last_order_item': last_order_item,
        'order': order,
        'tmat': tmat

    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="app/invoice.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def search(request):
    q = request.GET.get('q')
    data = Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request, 'app/search.html', {'data': data})



