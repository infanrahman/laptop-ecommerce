from django.urls import path
from .views import *

urlpatterns = [

    path('',home,name="home"),
    path('signup',signup,name="signup"),
    path('userlogin',userlogin,name="userlogin"),
    path('userlogout',userlogout,name="userlogout"),



    
    path('viewproduct',viewproduct,name="viewproduct"),
    path('cart',cart,name="cart"),
    path('shop_page',shop_page,name="shop_page"),
    path('productfilter/<str:data>',productfilter,name="productfilter"),
    path('addCart/<str:pk>',addCart,name="addCart"),
    path('ViewCart',ViewCart,name="ViewCart"),
    path('deleteCartItem/<str:pk>',deleteCartItem,name="deleteCartItem"),
    path('addQuantity/<str:pk>',addQuantity,name="addQuantity"),
    path('minusQuantity/<str:pk>',minusQuantity,name="minusQuantity"),
    path('productdetails/<str:pk>',productdetails,name="productdetails"),
    path('addtowhitelist/<str:pk>',addtowhitelist,name="addtowhitelist"),
    path('removewhitelist/<str:pk>',removewhitelist,name="removewhitelist"),
    path('whitelist',whitelist,name="whitelist"),
    path('checkout_page',checkout_page,name="checkout_page"),
    path('profile_page',profile_page,name="profile_page"),
    path('createAddress',createAddress,name="createAddress"),
    path('profilepic',profilepic,name="profilepic"),
    path('change_current_Password',change_current_Password,name="change_current_Password"),
    path('coupon_validation',coupon_validation,name="coupon_validation"),
    path('orderplaced',orderplaced,name="orderplaced"),
    path('payment_done',payment_done,name="payment_done"),
    path('checkout',checkout,name="checkout"),
    path('filter_product',filter_product,name="filter_product"),
    path('filter_shop/<str:data>',filter_shop,name="filter_shop"),
    path('brand/<str:data>',brand,name="brand"),
    path('deletepic',deletepic,name="deletepic"),
    path('base',base,name="base"),
    path('filterlaptype/<str:data>',filterlaptype,name="filterlaptype"),
    path('filterbrand/<str:data>',filterbrand,name="filterbrand"),
    path('success/',success,name="success"),
    path('failed/',failed,name="failed"),
    path('orders/',orders,name="orders"),
    path('cancel_order/<str:pk>',cancel_order,name="cancel_order"),
    path('cancelorder/<str:pk>',cancelorder,name="cancelorder"),
    path('refund/',refund,name="refund"),
    path('searchproduct/',searchproduct,name="searchproduct"),
    

]