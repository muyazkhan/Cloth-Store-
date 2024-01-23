from django.urls import path
from .views import ProductDetailsView,ProductReviewView

urlpatterns = [
    path('Details/<int:id>/', ProductDetailsView.as_view(), name='product_details'),
    path('review/<int:id>/', ProductReviewView.as_view(), name='product_review')
]
