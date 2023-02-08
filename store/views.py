from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User 
from .models import *
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.conf import settings
import razorpay
from django.db.models import Q


def signup(request):
    if request.method == 'POST':
        frist_name=request.POST['frist_name']
        username=request.POST['username']
        Email=request.POST['email']
        if User.objects.filter(username=username):
            messages.warning(request, 'Username is already exist')
            return redirect('signup')
        else:
            password=request.POST['password']
            corfirm_password=request.POST['repassword']
            if password==corfirm_password:
                              user=User.objects.create_user(
                                first_name=frist_name,
                                username=username,
                                email=Email,
                                password=password

                                    
                              )
                              user.save()
                              return redirect('userlogin')
    return render(request,'signup.html')

# userlogin

def userlogin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        try:
            user=User.objects.get(username=username)
        except:
                messages.warning(request, 'User is Not Exist')

    
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request, f'Hi {user.username}, Welcome To GETLAPS')
            return redirect('home')
        else:
            messages.warning(request, 'invalid Credential')
    
    return render(request,'login.html')






def userlogout(request):
    logout(request)
    return redirect('home')


def home(request):
    user=request.user
    product=Product.objects.filter(display=True)    
    if user.is_authenticated:
        whitelist_count=Whitelist.objects.filter(user=user).count()
        cart_count=Cart.objects.filter(user=user).count()
        print('0000000000000000000000000000',cart_count)   
        profile_photo=UserPhoto.objects.filter(user=request.user)  

        product_gaming=Product.objects.filter(lap_type='Gaming Laptop')
        brand=Brand.objects.all()
        context={'product':product,'brand':brand,'product_gaming':product_gaming,'cart_count':cart_count,'whitelist_count':whitelist_count,'profile_photo':profile_photo}
    else:
        product=Product.objects.all()
        product_gaming=Product.objects.filter(lap_type='Gaming Laptop')
        brand=Brand.objects.all()
        context={'product':product,'brand':brand,'product_gaming':product_gaming}
    return render(request,'home.html',context)

def base(request):
    username=request.user
    if request.user.is_authenticated:
        whitelist_count=Whitelist.objects.filter(user=username).count()
        cart_count=Cart.objects.filter(user=username).count()
        profile_photo=UserPhoto.objects.filter(user=username)  

    context={'cart_count':cart_count,'whitelist_count':whitelist_count,'profile_photo':profile_photo}
    return render(request,'base.html',context)




def viewproduct(request):
    return render(request,'view-products.html')


def cart(request):
    return render(request,'cart.html')

def searchproduct(request):
    context={}
    if request.method == 'POST':

        q = request.GET.get('q')
        
    return render(request,'shop.html',context)


def shop_page(request):
    search_product=''
    context={}
    product=Product.objects.all()
    if request.method == 'GET':
        q = request.GET.get('q')
        print(q)
        if q:
            search_product = Product.objects.filter(Lap_name__icontains=q)
        # Q(Lap_name=q) |
        # Q(lap_type__icontains=q) |
        # Q(brand__name__icontains=q)
          
            print(search_product)
            # return redirect('shop_page')
        
    if request.method =='POST':
        price=request.POST['price']
        if price:
            print('111111111111111111111111111111111111111111111111111111111111')
            print(price)
            product=Product.objects.filter(discounted_price__lte=price)
            print(price)
        else:
            product=Product.objects.filter(brand__icontains=brand)
    if not search_product:
        context={'product':product}
    else:
        context={'search_product':search_product}

    print(context)
    
    return render(request,'shop.html',context)


def filterlaptype(request,data='None'):
    if data == 'None':
        product=Product.objects.all()
    else:
        product=Product.objects.filter(lap_type__icontains=data)
    context={'product':product}
    return render(request,'shop.html',context)


def filterbrand(request,data='None'):
    if data == 'None':
        product=Product.objects.all()
    else:
        brand_iden=Brand.objects.get(brand_name=data)
        product=Product.objects.filter(brand=brand_iden)


    context={'product':product}
    return render(request,'shop.html',context)



def filter_shop(request,data='None'):
    print(data)
    if data == 'None':
        product=Product.objects.all()
    else:
        product=Product.objects.filter(lap_type=data)
        print("11111111111111111111111111111111111111111111")
        print(data)


    context={'product':product}
    return render(request,'shop.html',context)


def addCart(request,pk):
    user=request.user
    product=Product.objects.get(id=pk)
    cart=Cart.objects.create(user=user,Lap_name=product)
    return redirect('ViewCart')
    return render(request, 'cart_new.html')

def ViewCart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for c in cart:
        value=c.quantity * c.Lap_name.discounted_price
        amount=value+amount
    context={'cart':cart,'amount':amount}
    return render(request, 'cart_new.html',context)



def deleteCartItem(request,pk):
    cart=Cart.objects.get(id=pk)
    cart.delete()
    return redirect('ViewCart')
    return render(request, 'cart_new.html')

def addQuantity(request,pk):
    cart=Cart.objects.get(id=pk)
    cart.quantity+=1
    cart.save()
    return redirect('ViewCart')
    return render(request,'cart_new.html')
    

def minusQuantity(request,pk):
    cart=Cart.objects.get(id=pk)
    cart.quantity-=1
    cart.save()
    return redirect('ViewCart')
    return render(request,'cart_new.html')







def productdetails(request,pk):
    product=Product.objects.get(id=pk)
    context={'product':product}
    return render(request,'view-products.html',context)





def addtowhitelist(request,pk):
    user=request.user
    product=Product.objects.get(id=pk)
    Whitelist.objects.create(user=user,Lap_name=product).save()
    return redirect('whitelist')
   

def whitelist(request):
    user=request.user
    whitelist=Whitelist.objects.filter(user=user)
    context={'whitelist':whitelist}
    return render(request,'whitelist.html',context)



def removewhitelist(request,pk):
    whitelist=Whitelist.objects.get(id=pk)
    whitelist.delete()
    return redirect('whitelist')
    return render(request, 'whitelist.html')



def productfilter(request, data=None):
    product = Product.objects.all()

    if data == None:
        proc = Product.objects.all()
    elif data == 'MSI' or data == 'ASUS' or data == 'Redmi' or data == 'realme':
        proc = Product.objects.filter(brand = data) 

    return render(request, 'shop.html', {'product': product, 'proc':proc,})






def checkout_page(request):
    if request.user:
        profile=Profile.objects.filter(user=request.user) 
        cart=Cart.objects.filter(user=request.user)
        

        amount=0
        for c in cart:
            value=c.quantity * c.Lap_name.discounted_price
            amount=value+amount

    context={'profile':profile,'cart':cart,'amount':amount}                         
    return render(request,'checkout.html',context)




def profile_page(request):
    
    


    profile=UserPhoto.objects.filter(user=request.user)     
    address=Profile.objects.filter(user=request.user)     

    context={'address':address,'profile':profile}
    return render(request,'profile.html',context)




def createAddress(request):
    if request.method == 'POST':
        address=Profile.objects.filter(user=request.user)     
        if address:
            address.delete()
            fname=request.POST['fname']
            lname=request.POST['lname']
            house=request.POST['house']
            localplace=request.POST['localplace']
            district=request.POST['district']
            state=request.POST['state']
            pin=request.POST['pin']
            email=request.POST['email']
            mobile=request.POST['mobile']
            profile=Profile.objects.create(
                user=request.user,
                last_name=lname,
                mobile=mobile,
                house_name=house,
                local_place=localplace,
                town_city=localplace,
                discrict=district,
                pin_code=pin
                )                                

                                    
            profile.save()
            return redirect('profile_page')
        else:
            fname=request.POST['fname']
            lname=request.POST['lname']
            house=request.POST['house']
            localplace=request.POST['localplace']
            district=request.POST['district']
            state=request.POST['state']
            pin=request.POST['pin']
            email=request.POST['email']
            mobile=request.POST['mobile']
            profile=Profile.objects.create(
                user=request.user,
                last_name=lname,
                mobile=mobile,
                house_name=house,
                local_place=localplace,
                town_city=localplace,
                discrict=district,
                pin_code=pin
                )                                

                                    
            profile.save()
            return redirect('profile_page')     
    profile=Profile.objects.filter(user=request.user)     
    context={'profile':profile}                                 
    return render(request,'add_address.html',context)


def profilepic(request):
    user=request.user
    if request.method == 'POST':
        pic=request.FILES['photoupload']
        profile=UserPhoto.objects.create(user=request.user,user_profile=pic)     
        profile.save()
    profile=UserPhoto.objects.filter(user=request.user)     
    
    return render(request,'profile.html',{'profile':profile})


def deletepic(request):
    profile=UserPhoto.objects.filter(user=request.user)    
    profile.delete() 
    return redirect('profile_page')




def change_current_Password(request):
    username=request.user
    currentpassword= request.user.password 
    if request.method == 'POST':
            cur_password=request.POST['currpass']
            new_password=request.POST['newpass1']
            confirm_password=request.POST['newpass']
            u = User.objects.get(username__exact=username)
            u.set_password(new_password)
            u.save()
    return render(request,'profile.html')





def coupon_validation(request):
    user=request.user
    flag=0
    c_amount=0
    if request.method =='POST':
        coupon=request.POST.get('coupon')
        try:
            coupon_obj=Coupon.objects.get(code=coupon)
            if coupon_obj.is_expired == 1:
                messages.warning(request,"Coupon Expire")
                flag=1
                return redirect('checkout')

            else:
                coupon_obj.is_expired=1
                c_amount=coupon_obj.amount
                coupon_obj.save()
                messages.success(request,"Coupon Applied")
                return redirect('checkout')

        except:
            messages.warning(request,"Invalid Coupon")
            return redirect('checkout')




    # q = request.GET.get('q') if request.GET.get('q') != None else ''

    # rooms = Room.objects.filter(
    #     Q(topic__name__icontains=q) |
    #     Q(name__icontains=q) |
    #     Q(description__icontains=q)
    # )





    
    username=User.objects.get(username=user)
    coupon_dic=Coupon.objects.all()
    print(coupon_dic)           
    cart=Cart.objects.filter(user=user)
    amount=0
    for c in cart:
        value=c.quantity * c.Lap_name.discounted_price
        amount=value+amount
    total=amount
    if flag==0:
        coupon_amount=amount-c_amount
        context={'coupon_amount':coupon_amount}
        print(coupon_amount,'0000000000000000000')
    
    context={'cart':cart,'coupon_dic':coupon_dic,'total':total}
    return redirect('checkout')
    return render(request,'checkout.html',context)





def orderplaced(request):
    print(request.user,'0000000000000000000000000')
    return render(request,'order_placed.html')


def checkout(request):
    coupon=''
    c_amount=0
    
    if request.user:
        profile=Profile.objects.filter(user=request.user) 
        cart=Cart.objects.filter(user=request.user)
        try:
            coupon=Coupon.objects.filter(
            Q(user=request.user) &
            Q(is_expired=0))
            print(coupon,"===========000000000000=======")  
        except:
            print('you dont have')
        

        amount=0
        for c in cart:
            value=c.quantity * c.Lap_name.discounted_price
            amount=value+amount

    context={'cart':cart,'amount':amount}   
    user=request.user
    # request.session['g_user']=request.user
    

    cart=Cart.objects.filter(user=user)
    famount=0
    i=0
    for c in cart:
        value=c.quantity * c.Lap_name.discounted_price
        famount=famount+value
        i+=1
    if request.method =='POST':
        coupon=request.POST.get('coupon')
        try:
            coupon_obj=Coupon.objects.get(code=coupon)
            if coupon_obj.is_expired == 1:
                messages.warning(request,"Coupon Expire")
                flag=1
                return redirect('checkout')

            else:
                coupon_obj.is_expired=1
                c_amount=coupon_obj.amount
                famount=famount-c_amount
                print(famount,'0000000====famount======-----')

                coupon_obj.save()
                messages.success(request,"Coupon Applied")
                

        except:
            messages.warning(request,"Invalid Coupon")
            return redirect('checkout')
    
    print(famount,'0000000====fffffffffffff======-----')
    
    if c_amount:

        famount=famount-c_amount
        print(famount,'======================')

    razoramount=int(famount*100)
    client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
    data={'amount':razoramount,"currency":"INR","receipt":"order_rcptid_12"}
    payment_response=client.order.create(data=data)
    order_id=payment_response['id']
    order_status=payment_response['status']
    if order_status == 'created':
        payment=Payment.objects.create(
            user=user,
            amount=famount,
            razorpay_order_id=order_id,
            razorpay_payment_status=order_status
        )
        payment.save()
    email=request.user.email
    print()
    context={'cart':cart,'famount':famount,'razoramount':razoramount,'email':email,'payment':payment,'profile':profile,'coupon':coupon,'i':i}
    return render(request,'checkout.html',context)




def success(request):
    return render(request,'success.html')


def failed(request):
    return render(request,'cart.html')





def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request,'orders.html',{'order_placed':order_placed})






def filter_product(request):
 
    return render(request,'shop.html')



def brand(request,data):
    brand=Brand.objects.get(id=data)
    product=Product.objects.filter(brand=brand)
    return render(request,'shop.html',{'product':product})



def payment_done(request):
    # g_user = request.session.get('g_user')
    name=request.POST['name']
    print(name)
    response=request.POST
    params_dict={
            'razorpay_order_id':response.get('razorpay_order_id'),
            'razorpay_payment_id':response.get('razorpay_payment_id'),
            'razorpay_signature':response.get('razorpay_signature')
      }
    client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
    print(params_dict)
    status=client.utility.verify_payment_signature(params_dict)
    print(status)
    print(params_dict.get("razorpay_order_id"))
    payment=Payment.objects.get(razorpay_order_id__icontains=params_dict.get("razorpay_order_id"))
    print(payment)
    payment.razorpay_payment_id=params_dict.get("razorpay_payment_id")
    payment.paid=True
    payment.save()
    print(name)
    username=User.objects.get(username=name)
    cart_product=Cart.objects.filter(user=username)
    print(cart_product,"888888888888888888888888888888888")
    
       
    for cart_p in cart_product:
        print("ppppp")
        orderplacer=OrderPlaced.objects.create(user=username,product=cart_p.Lap_name
        ,quantity=cart_p.quantity,payment=payment,status="Accepted").save()
    cart_product.delete()
    return redirect('orders')
    return render(request,'checkout.html')




def cancel_order(request,pk):
    orderplac=OrderPlaced.objects.get(id=pk)
    p=Product.objects.get(id=orderplac.product_id)
    refund=Refund.objects.create(user=request.user,product=p,quantity=orderplac.quantity,
    total=orderplac.quantity* orderplac.product.discounted_price)
    print(refund,"0000000000000000000")
    orderplac.delete()

    return render(request,'order_placed.html',{'refund':refund,'p':p})

def cancelorder(request,pk):
    # orderplac=OrderPlaced.objects.get(id=pk)
    # p=Product.objects.get(id=orderplac.product_id)
    # refund=Refund.objects.create(user=request.user,product=p,quantity=orderplac.quantity,
    # total=orderplac.quantity* orderplac.product.discounted_price)
    # print(refund,"0000000000000000000")
    order_placed=OrderPlaced.objects.filter(user=request.user)
    orderplac=OrderPlaced.objects.get(id=pk)


    return render(request,'order_placed.html',{'order_placed':order_placed,'p':p})


def refund(request):
    refund=Refund.objects.filter(user=request.user)
    print(refund)
    return render(request,'refund.html',{'refund':refund})

