#from Projects.Project2.commerce.auctions.views import listings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.forms import ModelForm
from django.conf import settings


class User(AbstractUser):
    pass

# class Category(models.Model):
#     category = models.CharField(max_length=40)

#     def __str__(self):
#         return f"{self.category}"

class Listing(models.Model):
    title = models.CharField(max_length=80)
    desc = models.CharField(max_length=400)
    price = models.FloatField()
    img = models.URLField(null=True,blank=True)
    bidnow = models.FloatField(null=True,blank=True)
    category = models.CharField(max_length=40)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listing_owner", null=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_winner", null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{[{self.title},{self.price},{self.category},{self.owner}]}"

    class Meta:
        ordering = ['-creation']

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids_listing")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_buyer", null=True, blank=True)
    bidnow = models.FloatField(null=True,blank=True)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f"Item: {self.listing} [Highest bid = {self.bidnow} by {self.buyer} ({self.creation})]"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments_listing")
    msg = models.CharField(max_length=1000)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_user")
    creation = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f"{self.commenter} commented '{self.msg}' on {self.listing} on {self.creation}"

    class Meta:
        ordering = ['-creation']
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    listing = models.ForeignKey(Listing, blank=True, null=True, on_delete=models.CASCADE, related_name="watchlistings")

    def __str__(self):
        return f"User: {self.user}, listing: {self.listing}"