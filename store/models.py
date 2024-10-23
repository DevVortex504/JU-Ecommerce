from django.db import models
from django.contrib.auth.models import User


class Listing(models.Model):

    title = models.CharField(max_length=64)
    price = models.IntegerField()
    discounted_price = models.IntegerField(blank=True, default=None)
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
    #comments = models.ForeignKey(Comments, on_delete=models.CASCADE, blank=True)
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
