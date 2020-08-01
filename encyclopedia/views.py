from django.shortcuts import render

from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    file = util.get_entry(title)
    if file is None:
        return render(request,"encyclopedia/error.html",{
            "title":title.capitalize()
        })

    html = markdown2.markdown(file)

    return render(request,"encyclopedia/title.html",{
        "title" : title.capitalize(),
        "content" : html
    })
    
    

