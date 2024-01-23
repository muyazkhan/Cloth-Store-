from django.db import models
from product_list.models import ClothingItem
from accounts.models import User



RATINGS = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)

class Review(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    rating = models.IntegerField(choices=RATINGS)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.clothing_item.name} - {self.rating}"


class AverageRating(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, primary_key=True)
    average_rating = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)

    def update_average_rating(self):
        reviews = self.clothing_item.reviews.all()
        total_ratings = sum([review.rating for review in reviews])
        if total_ratings > 0:
            self.average_rating = total_ratings / len(reviews)
            self.total_reviews = len(reviews)
            self.save()
        else:
            self.average_rating = 0
            self.total_reviews = 0
            self.save()