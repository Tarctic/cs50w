from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment, Watchlist
from .forms import ListForm

def index(request):
    categories = ['None','Electronics','Toys','Garments','Footwear','Rare Collections','Antique Items','Furniture']

    return render(request, "auctions/index.html",{
        "alistings": Listing.objects.filter(active=True),
        "nalistings": Listing.objects.filter(active=False),
        "categories": categories,
    })


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

@login_required
def listings(request):
    categories = ['None','Electronics','Toys','Garments','Footwear','Rare Collections','Antique Items','Furniture']

    if request.method=="GET":
        return render(request, "auctions/listing.html", {
            "categories" : categories,
            "listform" : ListForm()
        })

    if request.method=="POST":
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        img = request.POST.get('img')
        category = request.POST.get('category')
        owner = request.user

        listing = Listing(title=title, desc=desc, price=price, img=img, category=category, owner=owner, bidnow=price, active=True)
        listing.save()

        bid = Bid(listing=listing, bidnow=price, buyer=owner)
        bid.save()

        return HttpResponseRedirect(reverse("index"))

def item(request, listing_id):
    if request.method=="GET":

        info = Listing.objects.get(pk=listing_id)
        id, title, desc, img = info.id, info.title, info.desc, info.img
        cat, date, active = info.category, info.creation, info.active
        owner, winner = info.owner, info.winner
        
        price = info.price
        bidnow = info.bidnow
        if bidnow == None:
            bidnow = price
            

        if img == None or img == '':
            img = "https://cdn-a.william-reed.com/var/wrbm_gb_food_pharma/storage/images/3/3/2/7/237233-6-eng-GB/Cosmoprof-Asia-Ltd-SIC-Cosmetics-20132_news_large.jpg"


        try:
            comments = Comment.objects.filter(listing=info)
        except Comment.DoesNotExist:
            comments=[]

        if request.user == owner:
            close = True
        else:
            close = False

        if active==False:
            if request.user == winner:
                win = True
            else:
                win = False

            if request.user == owner:
                own = True
            else:
                own = False
        else:
            win = None
            own = False

        if request.user.id==None:
            watch = False
        else:
            watch = True

        return render(request, "auctions/item.html",{
            "id": id, "title": title, "desc": desc, "img": img, 
            "price": price, "bidnow": bidnow,
            "cat": cat, "owner": owner, "date": date,
            "comments": comments,
            "active": active, "close" : close, 
            "win": win, 'winner': winner, "own": own, "watch": watch,
        })

    if request.method=="POST":
        newbid = request.POST.get('newbid','')
        listing = Listing.objects.get(id=listing_id)

        msg = request.POST.get('msg','')

        wishlist = request.POST.get('wish_list','')

        close = request.POST.get('close','')

        bid = Bid.objects.get(listing=listing)

        if newbid != '':

            if bid.buyer==listing.owner: 

                if float(newbid) >= bid.bidnow:
                    bid.bidnow = newbid
                    bid.buyer = request.user

                else:
                    return render(request, "auctions/error.html",{
                        "title": 'Error:',
                        "message": 'The value entered is lower than the starting price',
                        "id": listing_id,
                    })

            else:

                if float(newbid) > bid.bidnow:
                    bid.bidnow = newbid
                    bid.buyer = request.user

                else:
                    return render(request, "auctions/error.html",{
                        "title": 'Error:',
                        "message": 'The value entered must be higher than the current bid',
                        "id": listing_id,
                    })

            bid.save()
            
            listing.bidnow = newbid
            listing.save()

        elif msg!='':
            
            commenter = request.user
            c = Comment(msg=msg, commenter=commenter, listing=listing)
            c.save()

        elif close == 'closed':
            listing.active = False
            listing.winner = bid.buyer
            listing.save()

            return HttpResponseRedirect(reverse('item', args=(listing_id,)))

        elif wishlist=='wishlist':
            Watchlist.objects.create(user=request.user, listing=listing)

        return HttpResponseRedirect(reverse('item', args=(listing_id,)))

@login_required
def wishlist(request):
    
    if request.method=="POST":
        wish = request.POST.get('remove')
        l = Listing.objects.filter(id=wish)
        lrem = l[0]
        wrem = Watchlist.objects.filter(listing=lrem, user=request.user)
        for i in wrem:
            i.delete()

        return HttpResponseRedirect(reverse('wishlist'))

    if request.method=="GET":

        alistings = Listing.objects.filter(watchlistings__in=Watchlist.objects.filter(user=request.user), active=True).distinct()
        nalistings = Listing.objects.filter(watchlistings__in=Watchlist.objects.filter(user=request.user), active=False).distinct()

        return render(request, "auctions/index.html",{
            "title": "Watchlist",
            "alistings": alistings,
            "nalistings": nalistings,
            "remove": True
        })

def category(request, cat):
    
    if request.method == "GET":
        title = "Category: {}".format(cat)
        categories = ['None','Electronics','Toys','Garments','Footwear','Rare Collections','Antique Items','Furniture']

        return render(request, "auctions/index.html", {
            "title": title,
            "alistings": Listing.objects.filter(category=cat, active=True),
            "nalistings": Listing.objects.filter(category=cat, active=False),
            "categories": categories,
        })

    if request.method == "POST":

        return HttpResponseRedirect(reverse('index'))