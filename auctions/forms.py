from django import forms
from .models import *


class ListingForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "cols": 100}))
    startingBid = forms.DecimalField()
    image_url = forms.URLField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 1, "cols": 100}),
    )
    category = forms.CharField(required=False)


class BidForm(forms.Form):
    bidValue = forms.DecimalField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Bid"}),
    )


class CommentForm(forms.Form):
    content = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Write a comment..."}),
    )
