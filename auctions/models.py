from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="won_listings", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - Current Price: {self.current_price}"

class Bid(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid of {self.price} by {self.user.username} on {self.auction_listing.title}"

class Comment(models.Model):
    text = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.auction_listing.title}: {self.text[:50]}"
