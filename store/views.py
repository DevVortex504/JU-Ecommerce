from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Watchlist, Comments, Listing, Review
from django.contrib.auth.models import User


class NewListingForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Listing
        fields = ["title", "description", "price", "discounted_price", "category", "listing_image"]

def index(request):
    return render(request, "store/index.html",{
        "listings": Listing.objects.filter(active_status=True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.warning(request, "Invalid username and/or password.")
            return render(request, "store/login.html")
            #return render(request, "store/login.html", {
            #    "message": "Invalid username and/or password."
            #})
    else:
        return render(request, "store/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.warning(request, "Passwords must match.")
            return render(request, "store/register.html")
            #return render(request, "store/register.html", {
            #    "message": "Passwords must match."
            #})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            
            messages.warning(request, "Username already taken.")
            return render(request, "store/register.html")
            #return render(request, "store/register.html", {
            #    "message": "Username already taken."
            #})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "store/register.html")
    

def listing(request, listing_id):
    
    item = Listing.objects.get(pk=int(listing_id))
    reviews = Review.objects.filter(listing=item)
    stars = 0
    for review in reviews:
        stars += (review.stars)/len(reviews)
        
    
    if request.method == "POST" and request.user.is_authenticated: 
        if content:=request.POST.get("content"):
            comment = Comments.objects.create(content=content, listing=item, user=request.user)
            messages.success(request, "Commented successfully.")                
    comments = Comments.objects.filter(listing=item)

    watchlist=None
    if request.user.is_authenticated:
        try:
            watchlist = Watchlist.objects.get(user=request.user, listing=item)
        except:
            watchlist=None
        if watchlist:
            messages.warning(request, "Watchlisted")

    return render(request,"store/listing.html",{
        "listing": item,
        "comments": comments,
        "watchlist": watchlist,
        "id": int(listing_id),
        "stars": round(stars,1),
    })

@login_required
def close_listing(request, id):
    listing = get_object_or_404(Listing, pk=id)
    if request.user.is_authenticated and request.user==listing.user:
        listing.active_status=False
        listing.save()
        messages.success(request, "Listing closed successfully")

    return redirect("listings", listing_id = id)

@login_required
def createlisting(request):
    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES or None)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
        else:
            return render(request, "store/new_listing.html",{
                "form": NewListingForm(form)
            })

    return render(request, "store/new_listing.html",{
        "form": NewListingForm()
    })

@login_required
def watchlist(request):    
    items = Watchlist.objects.filter(user = request.user).all()
    n = len(items)
    return render(request, "store/watchlist.html",{
        "items": items,
    })

@login_required
def watchlist_add(request, id:int):

    #message = None
    id = int(id)
    listing = get_object_or_404(Listing, pk=id)
    user = request.user

    if Watchlist.objects.filter(user = user, listing = listing):
       # message = "Listing already added to watchlist"
        messages.warning(request, "Listing already added to watchlist.")
    else:
        watchlist = Watchlist(user = user, listing = listing)
        watchlist.save()
        #message = "Added to watchlist"
        messages.success(request, "Added to watchlist.")
    return redirect("listings", listing_id = id)

@login_required
def watchlist_remove(request, id:int):
    listing = get_object_or_404(Listing, pk=id)
    watchlist=Watchlist.objects.get(user=request.user, listing=listing)
    watchlist.delete()
    return redirect("listings", listing_id = id)


def categories(request):
    category_list = []
    categories = Listing.objects.filter(active_status=True)
    for category in categories:
        if category not in category_list:
            category_list.append(category.category)
    print(category_list)

    return render(request, "store/categories.html",{
        "categories": category_list,
    })

def category_listing(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request, "store/category_listing.html",{
        "listings": listings,
    })