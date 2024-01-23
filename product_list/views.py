from django.views.generic import ListView,TemplateView,CreateView
from django.views import View
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import UserAccount,User
from .models import ClothingItem,Wishlist,ShoppingCart
from .forms import ClothingFilterForm,UpdateForm
from django.contrib import messages
from django.shortcuts import redirect,render
from django.views import View
from django.utils import timezone
from django.db import IntegrityError

class ClothingListView(ListView):
    model = ClothingItem
    template_name = 'product.html'
    context_object_name = 'clothing_items'
    paginate_by = 6

    def get_queryset(self):
        queryset = ClothingItem.objects.all()

        size = self.request.GET.get('size')
        color = self.request.GET.get('color')

        if size:
            queryset = queryset.filter(size=size)
        if color:
            queryset = queryset.filter(color=color)
        return queryset.order_by('-popularity', 'price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ClothingFilterForm(self.request.GET)
        context['filter'] = form
        return context

class ProductWishlist(LoginRequiredMixin, ListView):
    model = ClothingItem
    template_name = 'wishlist.html'
    context_object_name = 'wishlist'

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Wishlist.objects.filter(user_id=user_id)
        return queryset

class WishlistView(LoginRequiredMixin, View):
    def get(self, request, id, **kwargs):
        item = get_object_or_404(ClothingItem, id=id)
        user = request.user
        try:
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=user,
                Clothing_item=item,
                defaults={'count': 1, 'date': timezone.now()}
            )
            if not created:
                wishlist_item.count += 1
                wishlist_item.save()
                messages.success(request, 'Product added to Wishlist successfully.')
            else:
                messages.success(request, 'Product added to Wishlist successfully.')
        except IntegrityError:
            wishlist_items = Wishlist.objects.filter(user=user, clothing_item=item)
            if wishlist_items.exists():
                wishlist_item = wishlist_items[0]
                wishlist_item.count += 1
                wishlist_item.save()
                messages.success(request, 'Product quantity in Wishlist updated.')
            else:
                messages.error(request, 'No matching item found in Wishlist.')

        return redirect('wishlist')

class DeleteWishlistView(LoginRequiredMixin, View):
    def get(self, request, id, **kwargs):
        try:
            item = ClothingItem.objects.get(id=id)
            user = request.user
            wishlist_items = Wishlist.objects.filter(user=user, Clothing_item=item)

            if wishlist_items.exists():
                wishlist_items.delete()
                messages.success(request, 'Product removed successfully from the wishlist')
            else:
                messages.warning(request, 'Product not found in the wishlist')
        except ClothingItem.DoesNotExist:
            messages.warning(request, 'Product not found')

        return redirect('wishlist')

class Product_Cart(LoginRequiredMixin, ListView):
    model = ClothingItem
    template_name = 'cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = ShoppingCart.objects.filter(user_id=user_id)
        return queryset

class CartView(LoginRequiredMixin, View):
    def get(self, request, id, **kwargs):
        item = get_object_or_404(ClothingItem, id=id)
        user = request.user

        try:
            cart_item, created = ShoppingCart.objects.get_or_create(
                user=user,
                Clothing_item=item,
                defaults={'count': 1, 'total_price': item.price, 'date': timezone.now()}
            )


            if not created:
                cart_item.count += 1
                cart_item.total_price = cart_item.count * item.price
                cart_item.save()
                messages.success(request, 'Product added to Cart successfully.')
            else:
                messages.success(request, 'Product added to Cart successfully.')

        except IntegrityError:
            cart_items = ShoppingCart.objects.filter(user=user, clothing_item=item)
            if cart_items.exists():
                cart_item = cart_items[0]
                cart_item.count += 1
                cart_item.total_price = cart_item.count * item.price
                cart_item.save()
                messages.success(request, 'Product quantity in Cart updated.')
            else:
                messages.error(request, 'No matching item found in Cart.')

        total_price = sum(cart.total_price for cart in ShoppingCart.objects.filter(user=user))

        return render(request, 'cart.html', {'cart_items': ShoppingCart.objects.filter(user=user), 'total_price': total_price})

class DeleteCartItem(LoginRequiredMixin,View):
    def get(self, request, id, **kwargs):
        try:
            item = ClothingItem.objects.get(id=id)
            user = request.user
            cart_item = ShoppingCart.objects.filter(user=user, Clothing_item=item)

            if cart_item.exists():
                cart_item.delete()
                messages.success(request, 'Product removed successfully from the cart')
            else:
                messages.warning(request, 'Product not found in the cart')
        except ClothingItem.DoesNotExist:
            messages.warning(request, 'Product not found')

        return redirect('cart')

class myAccountView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'myaccount.html')

class BuyProduct(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        user = request.user
        cart_items = ShoppingCart.objects.filter(user=user)

        if not cart_items:
            messages.info(request, 'Your cart is empty. Please add products to your cart.')
            return redirect('cart')

        total_cost = sum(cart_item.total_price for cart_item in cart_items)

        if user.account.balance >= total_cost:
            user.account.balance -= total_cost
            user.account.save(update_fields=['balance'])

            for cart_item in cart_items:
                cart_item.date = timezone.now()
                cart_item.save(update_fields=['date'])

            cart_items.delete()
            messages.success(request, 'Products bought successfully.')
            return render(request, 'orderdetails.html', {'user': user})
        else:
            messages.warning(request, 'Insufficient balance to buy products. Please contact site admin.')
            return redirect('cart')

class MyOrderDetails(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        user = request.user
        order_items = ShoppingCart.objects.filter(user=user)
        total_cost = sum(cart_item.total_price for cart_item in order_items)

        context = {
            'user': user,
            'order_items': order_items,
            'total_price': total_cost,
        }
        return render(request, 'orderdetails.html', context)


class AccountUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form = UpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('update_profile')
        return render(request, self.template_name, {'form': form})