from django.urls import path
from .views import ClothingListView,CartView, WishlistView,ProductWishlist,DeleteWishlistView,Product_Cart,DeleteCartItem,BuyProduct,MyOrderDetails, myAccountView,AccountUpdateView
urlpatterns = [
    path('product/',ClothingListView.as_view(),name="product"),
    path('wishlist/',ProductWishlist.as_view(),name="wishlist"),
    path('cart/',Product_Cart.as_view(),name="cart"),
    path('wishlist/<int:id>/', WishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<int:id>/', DeleteWishlistView.as_view(), name='remove_from_wishlist'),
    path('cart/remove/<int:id>/', DeleteCartItem.as_view(), name='remove_from_cart'),
    path('cart/<int:id>/', CartView.as_view(), name='add_to_cart'),
    path('myaccount1/',BuyProduct.as_view(),name="myaccount1"),
    path('myaccount/', myAccountView.as_view(),name="myaccount"),
    path('myaccount/MyOrderDetails/',MyOrderDetails.as_view(),name="MyOrderDetails"),
    path('myaccount/MyOrderDetails/update_account',AccountUpdateView.as_view(), name="update_profile"),
]
