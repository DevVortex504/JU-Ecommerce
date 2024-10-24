from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Listing(models.Model):

    title = models.CharField(max_length=64)
    price = models.PositiveIntegerField()
    discounted_price = models.PositiveIntegerField(blank=True, default=None)
    description = models.CharField(max_length=300, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    CATEGORY_CHOICES = [
        ('Tshirt', 'Tshirt'),
        ('Hoodie', 'Hoodie'),
        ('Back Printed', 'Back Printed'),
    ]
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES, blank=True)
    listing_image = models.ImageField(upload_to="images/", blank=True)
    active_status=models.BooleanField(default=True)
    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
class Comments(models.Model):
       
    content = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments", default = 1)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", default = 1)
    #commented_by = models.ManyToManyField(User, related_name="user_comments")

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlisted_user")

class Review(models.Model):
    stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    content = models.CharField(max_length=500, blank=True)
    images = models.ManyToManyField('ReviewImage', blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reviews")
    class Meta:
        unique_together = ('listing', 'user')

class ReviewImage(models.Model):
    image = models.ImageField(upload_to="review_images/")
