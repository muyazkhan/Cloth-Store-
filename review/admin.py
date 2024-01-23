from django.contrib import admin
from .models import Review,AverageRating
# Register your models here.
admin.site.register(Review)
admin.site.register(AverageRating)