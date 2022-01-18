from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime


class User(AbstractUser):
    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=64, null=True)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=64, null=True)
    currentBid = models.DecimalField(decimal_places=2, max_digits=10000, null=True)
    dateCreated = models.DateTimeField(default=datetime.now, null=True)
    description = models.CharField(max_length=300, null=True)
    startingBid = models.DecimalField(decimal_places=2, max_digits=10000, null=True)
    status = models.BooleanField(default=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    value = models.DecimalField(decimal_places=2, max_digits=10000, null=True)
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="bids"
    )
    listing = models.ForeignKey(
        Listing, null=True, on_delete=models.CASCADE, related_name="bids"
    )

    def __str__(self):
        return f"{self.user} offers {self.value} on {self.listing}"


class Comment(models.Model):
    content = models.CharField(max_length=500, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} Commented on {self.listing}"


class Watchlist(models.Model):
    users = models.ManyToManyField(User, blank=True)
    listings = models.ManyToManyField(Listing, blank=True)

    def __str__(self):
        # return f"{self.users} is interested in  {self.listings}"
        return str(self.id)
