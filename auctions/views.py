from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.urls import reverse
from decimal import Decimal, InvalidOperation

from .forms import AuctionListingForm
from .models import User, AuctionListing, Bid

def index(request):
    listings = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", { "listings": listings })


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
    
def create_listing(request):
    form = AuctionListingForm()

    if request.method == "POST":
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.current_price = request.POST["starting_bid"]

            listing.save()
            return redirect("index")
        else:
            form = AuctionListingForm()

    return render(request, "auctions/create_form.html", { "form": form })

@login_required(login_url="login")
def listing_page(request, id):
    listing = get_object_or_404(AuctionListing, pk=id)
    highest_bid_obj = listing.bids.order_by('-price', '-created_at').first()
    current_highest_price = highest_bid_obj.price if highest_bid_obj else listing.current_price
    no_of_bids = listing.bids.count()

    if listing.current_price != current_highest_price:
        listing.current_price = current_highest_price
        listing.save()

    if request.method == "POST":
        if request.user == listing.user:
            messages.error(request, "You cannot bid on your own listing.")
            return redirect("listing_page", id)

        try:
            new_bid_price = Decimal(request.POST["bid"])
        except(ValueError, TypeError, InvalidOperation):
            messages.error(request, "Invalid bid amount. Please enter a valid number.")
            return redirect("listing_page", id)

        if new_bid_price <= current_highest_price:
            messages.error(request, f"Your bid must be higher than the current highest bid (${current_highest_price:.2f}).")
            return redirect("listing_page", id)
        
        if new_bid_price < listing.starting_bid:
            messages.error(request, f"Your bid must be at least the starting bid (${listing.starting_bid:.2f}).")
            return redirect("listing_page", id)
        
        Bid.objects.create(price=new_bid_price, user=request.user, auction_listing=listing)

        listing.current_price = new_bid_price
        listing.save()

        messages.success(request, f"Your bid of ${new_bid_price:.2f} has been placed!")
        return redirect("listing_page", id)
    
    return render(request, "auctions/listing.html", { 
        "listing": listing,
        "no_of_bids": no_of_bids
    })
