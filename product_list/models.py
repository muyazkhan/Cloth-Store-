from django.db import models
from accounts.models import User
RATINGS = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)
SIZE =[('', 'Any'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large')]
COLORS =[('White','White'),('Black','Black'),('Blue','Blue')]

class category(models.Model):
    name = models.CharField("Name", max_length=100, default=None)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    def __str__(self):
        return self.name


class ClothingItem(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    popularity = models.IntegerField(default=0)
    description = models.TextField()
    size = models.CharField(max_length=10,choices=SIZE)
    color = models.CharField(max_length=20,choices=COLORS)
    image = models.ImageField(upload_to='product_list/media/clothing_images/',blank = True, null = True)
    
    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)
    Clothing_item = models.ForeignKey(ClothingItem,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'Clothing_item')

    def __str__(self):
         return f"{self.user.username}'s Cart Item"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    Clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'Clothing_item')

    def __str__(self):
        return f"{self.user.username}'s Wishlist Item"
