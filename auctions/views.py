from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from django import forms

from .models import User, Listing, Comment, Bid, category_names,\
                    dictCategoryChoices, revDictCategoryChoices, decToString

# ====================================================================== Classes
# ============================================================ Class ListingForm
class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('title', 'description', 'bid', 'picture', 'category')
        labels = {
            'title': "",
            'description': "",
            'bid': "",
            'picture': "",
            'category': "",
        }
        category_choices = ()
        widgets = {
            'title': forms.Textarea(
                attrs = {
                    'class': 'noresize',
                    'rows': '1',
                    'cols': '100',
                    'placeholder': 'Enter the title...'
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'rows': '8',
                    'cols': '100',
                    'placeholder': 'Enter the decription...'
                }
            ),
            'bid': forms.NumberInput(
                attrs = {
                    'placeholder': 'Enter the starting bid...'
                }
            ),
            'picture': forms.Textarea(
                attrs = {
                    'class': 'noresize',
                    'rows': '1',
                    'cols': '100',
                    'placeholder': 'Enter the URL of a picture (optional)...'
                }
            ),
            'category': forms.Select(choices = category_choices)
        }

# ============================================================ Class CommentForm
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        labels = {'comment': ""}
        widgets = {
            'comment': forms.Textarea(
                attrs = {
                    'class': 'comment-form',
                    'rows': '2',
                    'cols': '30',
                    'placeholder': 'Enter your comment...'
                }
            )
        }

# ================================================================ Class BidForm
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('amount',)
        labels = {'amount': ""}
        widgets = {
            'amount': forms.NumberInput(
                attrs = {
                    'class': 'bid-form',
                    'rows': '1',
                    'cols': '1',
                    'placeholder': 'Enter your max bid'
                }
            )
        }

    def associate_listing(self, listing_id):
        self.listing = Listing.objects.get(pk=listing_id)

    def clean(self):
        cleaned_data = super().clean()
        all_bids = self.listing.bids.all()
        amount = cleaned_data.get("amount")

        if all_bids.exists():
            max_amount = all_bids.aggregate(Max('amount'))['amount__max']
            if amount <= max_amount:
                msg = "New bid must be superior than the latest one."
                self.add_error("amount", msg)
        else:
            max_amount = self.listing.bid
            if amount < max_amount:
                msg = "First bid must be superior or equal to the original price."
                self.add_error("amount", msg)

# ============================================================= Define functions
# ===================================================== signed in user functions
def isLoggedIn(user):
    if user.is_authenticated:
        return User.objects.get(username=user.username)
    else:
        return None

def listingByUser(user):
    if user.is_authenticated:
        return User.objects.get(username=user.username).listings.all()
    else:
        return None

# ======================================================================== Index
def index(request):
    allListings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "fullNameCategory": dictCategoryChoices,
        "activeListings": reversed(allListings),
        "current_user": isLoggedIn(request.user),
        "listingsByUser": listingByUser(request.user),
        "page_name": "All Listings"
    })

# ============================================================= searchByCategory
def searchByCategory(request, categoryName):

    return render(request, "auctions/index.html", {
        "fullNameCategory": dictCategoryChoices,
        "activeListings": reversed(Listing.objects.all().filter(category__exact = revDictCategoryChoices[categoryName])),
        "current_user": isLoggedIn(request.user),
        "listingsByUser": listingByUser(request.user),
        "page_name": categoryName
    })

# =================================================================== Mylistings
def mylistings(request):

    return render(request, "auctions/index.html", {
        "fullNameCategory": dictCategoryChoices,
        "activeListings": reversed(User.objects.get(username=request.user.username).listings.all()),
        "current_user": isLoggedIn(request.user),
        "listingsByUser": listingByUser(request.user),
        "page_name": "My Listings"
    })

# ==================================================================== Watchlist
def watchlist(request):

    return render(request, "auctions/index.html", {
        "fullNameCategory": dictCategoryChoices,
        "activeListings": (User.objects.get(username=request.user.username).watching.all()),
        "current_user": isLoggedIn(request.user),
        "listingsByUser": listingByUser(request.user),
        "page_name": "My Watchlist"
    })

# ================================================================= Auctions Won
def auctions_won(request):
    return render(request, "auctions/index.html", {
        "fullNameCategory": dictCategoryChoices,
        "activeListings": (User.objects.get(username=request.user.username).won.all()),
        "current_user": isLoggedIn(request.user),
        "listingsByUser": listingByUser(request.user),
        "page_name": "Auctions Won"
    })

# ======================================================================== Login
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
                "message": "Invalid username and/or password.",
                "categories": category_names
            })
    else:
        return render(request, "auctions/login.html")

# ======================================================================= Logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# ===================================================================== Register
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

# ======================================================================= Create
def create(request):
    if request.method == "POST":
        newListing = ListingForm(request.POST)
        listing = Listing()

        if newListing.is_valid():
            listing.title = newListing.cleaned_data["title"]
            listing.description = newListing.cleaned_data["description"]
            listing.picture = newListing.cleaned_data["picture"]
            listing.category = newListing.cleaned_data["category"]
            listing.bid = newListing.cleaned_data["bid"]
            listing.user = User.objects.get(username=request.user.username)

            listing.save()

            # redirect towards created page
            return HttpResponseRedirect(reverse('listing', args=(listing.id, )))

    else:
        newListing = ListingForm()

    return render(request, "auctions/create.html", {
        "listing_form": newListing
    })

# ====================================================================== Listing
def listing(request, listing_id):
    id = int(listing_id)
    listing = Listing.objects.get(pk=id)
    fullNameCategory = dictCategoryChoices
    activeListings = listingByUser(request.user)
    newComment = CommentForm()
    bidding = BidForm()

    if activeListings is not None:
        createdByUser = listing in activeListings
    else:
        createdByUser = listing

    # Check if the request path is coming from bidding, commenting, closing or listing
    pathInfoSplit = request.path_info.split("/")

    if "bidding" in pathInfoSplit and request.method == "POST":
        bids = Bid()
        bidding = BidForm(request.POST)
        bidding.associate_listing(id)

        if bidding.is_valid():
            current_username = request.user.username
            bids.user = User.objects.get(username=current_username)
            bids.listing = Listing.objects.get(pk=id)
            bids.amount = bidding.cleaned_data["amount"]
            bids.save()
            bidding = BidForm()

            return HttpResponseRedirect(reverse('listing', args=(listing.id, )))

    elif "commenting" in pathInfoSplit and request.method == "POST":
        newComment = CommentForm(request.POST)
        comments = Comment()

        if newComment.is_valid():
            comments.comment = newComment.cleaned_data["comment"]
            comments.user = User.objects.get(username=request.user.username)
            comments.listing = Listing.objects.get(pk=listing_id)
            comments.save()
            newComment = CommentForm()

            return HttpResponseRedirect(reverse('listing', args=(listing_id, )))

    elif "closing" in pathInfoSplit and request.method == "POST":
        listing.winner = listing.bids.all().order_by("-amount").first().user
        listing.save()
        return HttpResponseRedirect(reverse('listing', args=(listing_id, )))

    commentsList = reversed(Comment.objects.filter(listing__exact= id))

    return render(request, "auctions/listing.html", {

        "title": Listing.objects.get(id__exact= id).title,
        "description": Listing.objects.get(id__exact= id).description,
        "bid": listing.currentBid(),
        "picture": Listing.objects.get(id__exact= id).picture,
        "category": fullNameCategory[Listing.objects.get(id__exact= id).category],

        "owner": Listing.objects.get(id__exact= id).user,
        "listing_id": Listing.objects.get(id__exact= id).id,
        "watching": listing.watchedby.filter(username=request.user.username).exists(),
        "createdByUser": createdByUser,

        "bid_form": bidding,
        "bid_count_sentence": f"{listing.bids.count()} bid{'s'[:(listing.bids.count())^1]}",
        "bid_count": listing.bids.count(),
        "original_price": Listing.objects.get(id__exact= id).bid,

        "winner": listing.winner,

        "comment_form": newComment,
        "comments_list": commentsList
    })

# ====================================== Watching (add or remove from watchlist)
def watching(request):

    if request.method == "POST":
        current_username = request.user.username
        current_user = User.objects.get(username=current_username)
        listingid = request.POST.get("listing")
        listing = Listing.objects.get(pk=listingid)
        watching = listing.watchedby.filter(username=current_username)
        is_watching = watching.exists()

        if is_watching:
            listing.watchedby.remove(current_user)

        else:
            listing.watchedby.add(current_user)

    return JsonResponse({})

# ======================================================================== About
def about(request):
    return render(request, "auctions/about.html")
