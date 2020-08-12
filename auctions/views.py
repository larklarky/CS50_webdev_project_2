from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import Listing, User, Bid, Wishlist
from .forms import BidForm, CreateListingForm




def index(request):
    listings = Listing.objects.filter(status = 'ACTIVE').order_by('-date_created')
    return render(request, "auctions/index.html", {
        'listings': listings, 
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")




def listing(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    time_left = listing.valid_until - listing.date_created
    bids_counter = listing.bids.count()
    user = request.user
    price = listing.price

    try:
        Wishlist.objects.get(user = user, listing = listing)
    except Wishlist.DoesNotExist:
        found_in_watchlist = False
    else:
        found_in_watchlist = True


    if bids_counter > 0:
        price = Bid.objects.filter(listing_id = listing_id).order_by('-bid')[0].bid
        # price = listing.bids.order_by('-bid')[0].bid


    if request.method == 'POST':
        bid_form = BidForm(request.POST)

        if bid_form.is_valid() and user.is_authenticated:
            bid = bid_form.cleaned_data['bid']
            if user == listing.user:
                messages.error(request, "You can't place bids on your own listings.")
            
            elif bids_counter == 0 and bid < price:
                messages.error(request, 'Your bid must be at least as large as the starting bid.')

            elif bids_counter > 0 and bid <= price:
                messages.error(request, 'Your bid must be greater then other bids.')
            else:
                new_bid = Bid(bid = bid, user = user, listing = listing)
                new_bid.save()
                listing = Listing.objects.get(id = listing_id)
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))

    return render(request, "auctions/listing.html", {
        "listing": listing,
        'bids': bids_counter,
        'price': price,
        'found_in_watchlist': found_in_watchlist,
    })



@login_required(login_url="/login")
def create_listing(request):
    create_form = CreateListingForm()

    if request.method == 'POST':
        create_form = CreateListingForm(request.POST, request.FILES)
        current_user = request.user

        if create_form.is_valid():
            title = create_form.cleaned_data['title']
            description = create_form.cleaned_data['description']
            image = create_form.cleaned_data['image']
            category = create_form.cleaned_data['category']
            valid_until = create_form.cleaned_data['valid_until']
            price = create_form.cleaned_data['price']
            user = current_user

            new_listing = Listing(title = title, description = description, image = image, 
            category = category, valid_until = valid_until, price = price, user = user)
            new_listing.save()
            listing_id = new_listing.id
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))       
            
    return render(request, 'auctions/create_listing.html', {
        'create_form': create_form,
    })


@login_required(login_url="/login")
def addToWatchlist(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    user = request.user
    watchlist_item = Wishlist(listing = listing, user = user)
    watchlist_item.save()
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))


@login_required(login_url="/login")
def removeFromWatchlist(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    user = request.user
    watchlist_item = Wishlist.objects.get(listing = listing, user = user)
    watchlist_item.delete() 
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))
