from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *


# @login_required
def index(request):
    allListings = Listing.objects.all()
    # print(f"active listings: {activeListings}")
    return render(request, "auctions/index.html", {"allListings": allListings})


@login_required
def activeListings(request):
    activeListings = Listing.objects.exclude(status=False).all()
    # print(f"active listings: {activeListings}")
    return render(
        request, "auctions/activeListings.html", {"activeListings": activeListings}
    )


@login_required
def userWatchlist(request):
    listings = []
    userWatchlistobjects = Watchlist.objects.filter(users=request.user)
    for userWatchlistobject in userWatchlistobjects:
        listings.append(userWatchlistobject.listings.get())
    return render(request, "auctions/userWatchlist.html", {"Listings": listings})


@login_required
def categories(request):
    allCategories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": allCategories})


@login_required
def getCategoryListings(request, category):
    listings = []
    categoryObj = Category.objects.get(name=category)
    templistings = Listing.objects.filter(categories=categoryObj)
    for listing in templistings:
        if listing.status:
            listings.append(listing)
    return render(
        request,
        "auctions/getCategoryListings.html",
        {"listings": listings, "category": category},
    )


@login_required
def viewListing(request, listingId):
    currentListing = Listing.objects.get(id=listingId)
    currentUser = User.objects.get(id=request.user.id)

    if Watchlist.objects.filter(users=currentUser, listings=currentListing):
        watchlist = True
    else:
        watchlist = False

    categories = []
    for category in currentListing.categories.all():
        categories.append(category.name)

    comments = Comment.objects.filter(listing=currentListing)

    closeAuction = False
    if currentUser.id == currentListing.user.id and currentListing.status == True:
        closeAuction = True

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            userBid = form.cleaned_data["bidValue"]
            maxBid = currentListing.currentBid
            minBid = currentListing.startingBid
            if maxBid:
                if userBid <= maxBid:
                    bidReview = "Error!!: Your Bid Isn't Enough to Get This Product "
                    return render(
                        request,
                        "auctions/viewListing.html",
                        {
                            "listing": currentListing,
                            "categories": categories or ["No Category Listed"],
                            "watchlist": watchlist,
                            "form": form,
                            "cform": CommentForm(),
                            "comments": comments,
                            "bidReview": bidReview,
                            "closeAuction": closeAuction,
                        },
                    )
                elif userBid > maxBid:
                    newBid = Bid.objects.create(
                        value=userBid, user=currentUser, listing=currentListing
                    )
                    newBid.save()
                    currentListing.currentBid = userBid
                    currentListing.save()
                    return render(
                        request,
                        "auctions/viewListing.html",
                        {
                            "listing": currentListing,
                            "categories": categories or ["No Category Listed"],
                            "watchlist": watchlist,
                            "closeAuction": closeAuction,
                            "form": BidForm(),
                            "cform": CommentForm(),
                            "comments": comments,
                        },
                    )
            else:
                if userBid < minBid:
                    bidReview = "Error!!: Your Bid Isn't Enough to Get This Product "
                    return render(
                        request,
                        "auctions/viewListing.html",
                        {
                            "listing": currentListing,
                            "categories": categories or ["No Category Listed"],
                            "watchlist": watchlist,
                            "closeAuction": closeAuction,
                            "form": form,
                            "cform": CommentForm(),
                            "comments": comments,
                            "bidReview": bidReview,
                        },
                    )
                elif userBid >= minBid:
                    newBid = Bid.objects.create(
                        value=userBid, user=currentUser, listing=currentListing
                    )
                    newBid.save()
                    currentListing.currentBid = userBid
                    currentListing.save()
                    return render(
                        request,
                        "auctions/viewListing.html",
                        {
                            "listing": currentListing,
                            "categories": categories or ["No Category Listed"],
                            "watchlist": watchlist,
                            "closeAuction": closeAuction,
                            "form": BidForm(),
                            "cform": CommentForm(),
                            "comments": comments,
                        },
                    )
        else:
            return render(
                request,
                "auctions/viewListing.html",
                {
                    "listing": currentListing,
                    "categories": categories or ["No Category Listed"],
                    "watchlist": watchlist,
                    "closeAuction": closeAuction,
                    "cform": CommentForm(),
                    "comments": comments,
                    "form": form,
                },
            )
    if currentListing.status == False and currentListing.currentBid:
        highestBid = Bid.objects.get(
            value=currentListing.currentBid, listing=currentListing
        )
        winner = highestBid.user
        return render(
            request,
            "auctions/viewListing.html",
            {
                "listing": currentListing,
                "categories": categories or ["No Category Listed"],
                "watchlist": watchlist,
                "closeAuction": closeAuction,
                "form": BidForm(),
                "cform": CommentForm(),
                "comments": comments,
                "winner": winner,
            },
        )
    return render(
        request,
        "auctions/viewListing.html",
        {
            "listing": currentListing,
            "categories": categories or ["No Category Listed"],
            "watchlist": watchlist,
            "closeAuction": closeAuction,
            "form": BidForm(),
            "cform": CommentForm(),
            "comments": comments,
        },
    )


@login_required
def addComment(request, listingId):
    currentListing = Listing.objects.get(id=listingId)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            commentContent = form.cleaned_data["content"]
            newComment = Comment.objects.create()
            newComment.content = commentContent
            newComment.user = request.user
            newComment.listing = currentListing
            newComment.save()
    return HttpResponseRedirect(reverse("viewListing", kwargs={"listingId": listingId}))


@login_required
def closeAuction(request, listingId):
    currentListing = Listing.objects.get(id=listingId)
    currentListing.status = False
    currentListing.save()
    return HttpResponseRedirect(reverse("viewListing", kwargs={"listingId": listingId}))


@login_required
def addToWatchlist(request, listingId):
    currentLiting = Listing.objects.get(id=listingId)
    newWl = Watchlist.objects.create()
    newWl.users.set([request.user])
    newWl.listings.set([currentLiting])

    return HttpResponseRedirect(reverse("viewListing", kwargs={"listingId": listingId}))


@login_required
def RemoveFromWatchlist(request, listingId):
    currentLiting = Listing.objects.get(id=listingId)
    currentWl = Watchlist.objects.get(users=request.user, listings=currentLiting)
    currentWl.delete()

    return HttpResponseRedirect(reverse("viewListing", kwargs={"listingId": listingId}))


@login_required
def createListing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            tit = form.cleaned_data["title"]
            desc = form.cleaned_data["description"]
            stBid = form.cleaned_data["startingBid"]
            i_url = form.cleaned_data["image_url"]
            cate = form.cleaned_data["category"]
            l = Listing.objects.create(
                user=request.user, title=tit, description=desc, startingBid=stBid
            )
            l.save()
            # check if image_url & category fields have a value as they are not required
            if i_url:
                l.image_url = i_url
                l.save()
            if cate:
                if Category.objects.filter(name=cate):
                    oldCate = Category.objects.get(name=cate)
                    l.categories.set([oldCate])
                    l.save()
                else:
                    newCate = Category.objects.create(name=cate)
                    l.categories.set([newCate])
                    l.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/createListing.html", {"form": form})

    return render(request, "auctions/createListing.html", {"form": ListingForm()})


# def placeBid(request, listingId):
#     pass


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


# @login_required
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
