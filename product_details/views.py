from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import DetailView,CreateView
from product_list.models import ClothingItem
from review.models import Review
from review.forms import ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse

class ProductDetailsView(LoginRequiredMixin,DetailView):
    template_name = 'clothing_item_detail.html'
    model = ClothingItem
    pk_url_kwarg = 'id'
    context_object_name = "cloth"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        item = ClothingItem.objects.get(pk=id)
        reviews = Review.objects.filter(clothing_item=item)
        context['reviews'] = reviews

        return context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     product = self.object

    #

    #     try:
    #         average_rating = AverageRating.objects.get(clothing_item=product)
    #         context['average_rating'] = average_rating.average_rating
    #     except AverageRating.DoesNotExist:
    #         context['average_rating'] = None
    #     return context


class ProductReviewView(LoginRequiredMixin,CreateView):
    template_name = 'product_review.html'
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy("product_review")

    def get_initial(self):
        id = self.kwargs['id']
        cloth = ClothingItem.objects.get(pk=id)
        initial = {'clothing_item': cloth, 'user': self.request.user}
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        cloth = ClothingItem.objects.get(pk=id)
        reviews = Review.objects.filter(clothing_item=cloth)
        context.update({
            'clothing_item': cloth,
            'reviews': reviews,
        })
        return context

    def form_valid(self, form):
        id = self.kwargs['id']
        cloth = ClothingItem.objects.get(pk=id)
        is_already_reviewed = Review.objects.filter(
            clothing_item=cloth, user=self.request.user).count()
        if is_already_reviewed >= 1:
            messages.info(self.request, "You have already reviewed this Product.")
            return redirect("product_review",id=cloth.id)
        else:
            messages.success(self.request, "Thanks for your valuable review.")
        return super().form_valid(form)



