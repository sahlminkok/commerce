from django.forms import ModelForm
from .models import AuctionListing

class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "starting_bid", "image"]
