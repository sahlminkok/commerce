from django import forms
from .models import AuctionListing

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "starting_bid", "image"]

        widgets = {
            "title": forms.TextInput(attrs={ "class": "form-control" }),
            "description": forms.Textarea(attrs={ "class": "form-control" }),
            "starting_bid": forms.NumberInput(attrs={ "class": "form-control" }),
            "image": forms.URLInput(attrs={ "class": "form-control" })
        }
