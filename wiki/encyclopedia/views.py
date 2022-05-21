from django.shortcuts import render, redirect
from . import util
from . import markdown2
from django.urls import reverse
import random 


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def newpage(request, name):
    info = util.get_entry(name)
    if info==None:
        return render(request, "encyclopedia/error.html",{
            "title" : "Error : 404",
            "message" : "The requested page does not exist."
        })
    else: 
        return render(request, "encyclopedia/page.html", {
            "title" : name, 
            "info" : markdown2.markdown(info)
        })

def search(request):
    key = str(request.POST.get('q')).lower()
    entries = util.list_entries()
    aentries=[]
    for entry in entries:
        if key in entry.lower():
            aentries.append(entry)
            if key == entry.lower():
                entry = aentries[0]
                info = util.get_entry(entry)
                return render(request, "encyclopedia/page.html", {
                    "title" : entry,
                    "info" : markdown2.markdown(info)
                })

    noe = len(aentries)
    if noe==0:
        return render(request, "encyclopedia/searchm.html")

    else:
        return render(request, "encyclopedia/searchm.html",{
            "entries" : aentries
        })

def create(request):
    if request.method=="GET":
        return render(request, "encyclopedia/create.html")
        
    elif request.method=="POST":
        title = request.POST.get('title')    
        info = request.POST.get('info')


        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "title" : "Error",
                "message" : "Title already exists. Please use a different title."
            })


        elif len(title)==0 or len(info)==0:
            return render(request, "encyclopedia/error.html", {
                "title" : "Error",
                "message" : "Title and information are required fields."
            })

        else:
            info = "# " + title + "\n" + info

            util.save_entry(title, info)

            return render(request, "encyclopedia/page.html", {
                "title" : title, 
                "info" : markdown2.markdown(info),
            })
                

def edit(request, name):
    if request.method=="GET":

        info = util.get_entry(name.lower())
        find = info.find("\n")
        length = len(info)
        info = info[find:length]

        return render(request, "encyclopedia/edit.html", {
            "title" : name,
            "info" : info
        })

    elif request.method=="POST":
        title = request.POST.get('title')    
        info = request.POST.get('info')

        if len(title)==0 or len(info)==0:
            return render(request, "encyclopedia/error.html", {
                "title" : "Error",
                "message" : "Title and information are required fields."
            })

        else:
            info = "# " + title + "\n" + info

            util.save_entry(title, info)

            return render(request, "encyclopedia/page.html", {
                "title" : title, 
                "info" : markdown2.markdown(info),
            })

def rand(request):
    entries = util.list_entries()
    num = len(entries)
    r = random.randint(0,(num-1))
    name = entries[r]
    info = util.get_entry(name)
    if info==None:
        return render(request, "encyclopedia/error.html",{
            "title" : "Error : 404",
            "message" : "The requested page does not exist."
        })
    else: 
        return render(request, "encyclopedia/page.html", {
            "title" : name, 
            "info" : markdown2.markdown(info)
        })
