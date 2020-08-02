from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import re

from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    if request.method == "GET":
        q = request.GET["q"]
        if util.get_entry(q) is not None:
            return HttpResponseRedirect(reverse('entry',args=(q,)))
        
        result=[]
        for title in util.list_entries():
            if q.upper() in title.upper():
                result.append(title)
        return render(request,"encyclopedia/search.html",{
            "matches" : result,
            "q" : q
        })


def entry(request,title):
    file = util.get_entry(title)
    if file is None:
        return render(request,"encyclopedia/error.html",{
            "title":title
        })

    html = markdown2.markdown(file)

    return render(request,"encyclopedia/title.html",{
        "title" : title,
        "content" : html
    })
    
    

