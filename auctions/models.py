from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models import Max
from django.core.validators import MinValueValidator, URLValidator

# Turn decimal into string with 2 decimal places
def decToString(number):
    return '{:.2f}'.format(number)


class User(AbstractUser):
    pass


class Listing(models.Model):

    category_choices = (
        ("CL", "Clothing"),
        ("JE", "Jewelries"),
        ("AC", "Accessories"),
        ("RE", "Records"),
        ("BO", "Books"),
        ("AR", "Artworks"),
        ("DE", "Decorations"),
        ("IN", "Patterns"),
        ("OT", "Others"),
        (None, "Choose a category...")
    )

    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 800)
    bid = models.DecimalField(max_digits = 8, decimal_places = 2, validators=[MinValueValidator(0.0)])
    picture = models.URLField(blank = True, max_length = 350, validators=[URLValidator()])
    category = models.CharField(default = None, choices = category_choices, max_length = 2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    watchedby = models.ManyToManyField(User, blank=True, related_name="watching")
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="won")

    def currentBid(self):
        all_bids = self.bids.all()

        if all_bids.exists():
            max_amount = all_bids.aggregate(Max('amount'))['amount__max']
        else:
            max_amount = self.bid

        return decToString(max_amount)


# Only the name of each category
category_names = [name[1] for name in Listing.category_choices][:-1]

# Store category choices in a dictionary
dictCategoryChoices = dict(Listing.category_choices)

# Reverse dictCategoryChoices mapping
revDictCategoryChoices = {value: key for key, value in Listing.category_choices}


class Comment(models.Model):
    comment = models.CharField(max_length = 800)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentedby")


class Bid(models.Model):
    amount = models.DecimalField(max_digits = 8, decimal_places = 2, validators=[MinValueValidator(0.0)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
