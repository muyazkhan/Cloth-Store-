from django.shortcuts import render
from django.views import View
from product_list.models import ClothingItem

class homeView(View):
    template_name = 'home.html'

    def get(self, request):
        cloth = ClothingItem.objects.all()
        return render(request, self.template_name, {"cloth":  cloth})
