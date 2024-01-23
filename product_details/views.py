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





# class DetailsPost(DetailView):
#     model = models.AddCourse
#     pk_url_kwarg = 'id'
#     template_name = 'CourseDetails.html'

#     def post(self,request,*args,**kwargs):
#         comment_form = forms.CommentForm(data = self.request.POST)
#         post = self.get_object()
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit = False)
#             new_comment.post = post
#             new_comment.save()
#         return self.get(request, *args,**kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.object
#         comments = post.comments.all()
#         comment_form = forms.CommentForm()

#         context['comments'] = comments
#         context['comment_form'] = comment_form
#         return context
# class AddReviewView(View):
#     template_name = 'clothing_item_detail.html'
#     form_class = ReviewForm

#     def get(self, request, pk):
#         clothing_item = get_object_or_404(ClothingItem, pk=pk)
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form, 'clothing_item': clothing_item})

#     def post(self, request, pk):
#         clothing_item = get_object_or_404(ClothingItem, pk=pk)
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.clothing_item = clothing_item
#             review.save()

#             # Update average rating
#             average_rating, created = AverageRating.objects.get_or_create(clothing_item=clothing_item)
#             average_rating.update_average_rating()

#             return redirect('product-details', id=clothing_item.id)

#         return render(request, self.template_name, {'form': form, 'clothing_item': clothing_item})
