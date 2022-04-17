from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE

# Create your models here.
STATE_CHOICES = (
    ('Dhaka', 'Dhaka'),
    ('Gazipur', 'Gazipur'),
    ('Tongi', 'Tongi'),
    ('Shavar', 'Shavar'),
    ('Uttara', 'Uttara'),
    ('Comilla', 'Comilla'),
    ('Rajshahi', 'Rajshahi'),
    ('Jamalpur', 'Jamalpur'),
    ('Bogura', 'Bogura'),
    ('Rongpur', 'Rongpur'),
    ('Maymanshing', 'Maymanshing'),
    ('Dinajpur', 'Dinajpur'),
    ('Kustia', 'Kustia'),
    ('Madaripur', 'Madaripur'),
    ('Khulna', 'Khulna'),
    ('Borishal', 'Borishal'),
    ('Norshingdi', 'Norshingdi'),

)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=70)
    Zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Loptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),

    ('CS', 'Cooking Essentials'),
    ('GG', 'General Grocery'),
    ('PC', 'Personal Care '),
    ('CU', 'Cleaning Utility'),
    ('B', 'Beverages'),

)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='productimg')
    product_stock = models.IntegerField(default=100, blank=True, null=True)

    def __str__(self):
        return str(self.title)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qunatity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.qunatity * self.product.discounted_price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancle'),
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    shipping_cost = models.FloatField(default=0)
    shipping_address = models.CharField(max_length=250, blank=True, null=True)
    

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qunatity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    shipping_address = models.CharField(max_length=250)
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', blank=True, null=True)
    

    @property
    def total_cost(self):
        return self.qunatity * self.product.discounted_price

    class Meta:
        ordering = ('ordered_date',)
        get_latest_by = ('ordered_date',)
        
        

        
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    sold_quantity = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.product.title

    @property
    def stock_available(self):
        total = self.product.product_stock-self.sold_quantity
        return total