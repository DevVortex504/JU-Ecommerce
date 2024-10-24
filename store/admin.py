from django.contrib import admin
from .models import Listing, Comments, Watchlist, Review

# Register your models here.
admin.site.register(Listing)
admin.site.register(Comments)
admin.site.register(Watchlist)
admin.site.register(Review)