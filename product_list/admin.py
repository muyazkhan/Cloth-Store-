from django.contrib import admin
from .models import ClothingItem,category,ShoppingCart,Wishlist
# Register your models here.
admin.site.register(ClothingItem)
class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
admin.site.register(category,categoryAdmin)
admin.site.register(ShoppingCart)
admin.site.register(Wishlist)
