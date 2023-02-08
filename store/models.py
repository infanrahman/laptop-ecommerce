from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL

# Create your models here.


CATEGORY_CHOICE=(
    ('Gaming Laptop','Gaming Laptop'),
    ('Office Laptop','Office Laptop'),
    ('Student Laptop','Student Laptop')
)


STATUS_CHOICE=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('Delivered','Delivered'),
    ('Pending','Pending'),
    ('Cancel','Cancel')
)

class Brand(models.Model):
    brand_name=models.CharField(max_length=200, null=True)
    brand_image=models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.brand_name


class Specification(models.Model):
    processor=models.CharField(max_length=200, null=True)
    ram=models.CharField(max_length=200, null=True)
    storage=models.CharField(max_length=200, null=True)
    os=models.CharField(max_length=200, null=True)
    color=models.CharField(max_length=200, null=True)
    size=models.CharField(max_length=200, null=True)


class Product(models.Model):
    Lap_name=models.CharField(max_length=200, null=True)
    lap_image=models.ImageField(null=True, blank=True)
    lap_type=models.CharField(choices=CATEGORY_CHOICE,max_length=100,null=True)
    discounted_price=models.IntegerField(null=True)
    actual_price=models.IntegerField(null=True)
    brand=models.ForeignKey(Brand, on_delete=models.CASCADE,null=True,blank=True)
    available_item=models.IntegerField(null=True,blank=True)
    description=models.CharField(max_length=200, null=True,blank=True)
    specification= models.ForeignKey(Specification, on_delete=models.SET_NULL,null=True,blank=True)
    display=models.BooleanField(default=False,null=True,blank=True)
    


    def __str__(self):
        return self.Lap_name



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    Lap_name = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.Lap_name.discounted_price



class Whitelist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    Lap_name = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)




class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    last_name=models.CharField(max_length=200, null=True)
    mobile=models.IntegerField( null=True)
    house_name=models.CharField(max_length=200, null=True)
    local_place=models.CharField(max_length=200, null=True)
    town_city=models.CharField(max_length=200, null=True)
    discrict=models.CharField(max_length=200, null=True)
    pin_code=models.CharField(max_length=200, null=True)



class UserPhoto(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL,null=True)
    user_profile=models.ImageField(null=True, blank=True)




class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    code=models.CharField(max_length=200, null=True)
    is_expired=models.IntegerField(default=0)
    amount=models.IntegerField(null=True)




class Payment(models.Model):
    user=models.ForeignKey(User ,on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)




class OrderPlaced(models.Model):
    user=models.ForeignKey(User ,on_delete=models.CASCADE)
    product=models.ForeignKey(Product ,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICE,default="Pending")
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price



class Refund(models.Model):
    user=models.ForeignKey(User ,on_delete=models.CASCADE)
    product=models.ForeignKey(Product ,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    total=models.IntegerField(null=True,blank=True)

