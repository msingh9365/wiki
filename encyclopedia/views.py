from django.shortcuts import render,redirect
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from django import forms
from . import util
import markdown2



class createPageForm(forms.Form):
    title = forms.CharField(
        label="Title", widget=forms.TextInput(attrs={"placeholder": "Title goes here"})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Content goes here"}),
        label="Content",
    )


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def search(request):
    if request.method == "GET":
        q = request.GET["q"]
        if util.get_entry(q) is not None:
            return HttpResponseRedirect(reverse("entry", args=(q,)))

        result = []
        for title in util.list_entries():
            if q.upper() in title.upper():
                result.append(title)
        return render(request, "encyclopedia/search.html", {"matches": result, "q": q})


def entry(request, title):
    file = util.get_entry(title)
    if file is None:
        return render(request, "encyclopedia/error.html", {"title": title})
    
    html = markdown2.markdown(file)

    return render(request, "encyclopedia/title.html", {"title": title, "content": html})




def create(request):
    if request.method == "POST":
        form = createPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]

            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                content = "#"+title + '\n' + content
                util.save_entry(title, content)
                return redirect("entry",title = title)
            else:

                return render(
                    request,
                    "encyclopedia/create.html",
                    {"form": form, "error": "File Already Exists! :("},
                )
        else:
            return render(request, "encyclopedia/create.html", {"form": form})

    return render(request, "encyclopedia/create.html", {"form": createPageForm()})

def edit(request,title):

    if request.method == "POST":
        form = createPageForm(request.POST)
        if form.is_valid():
            head,content = form.cleaned_data["title"],form.cleaned_data["content"]
            print(content)
            content = "#"+head + '\n' + content
            content = content.replace('\r','')
            util.save_entry(head,content)
            return redirect("entry",title = head)

    content = util.get_entry(title)
    content = content[content.find('\n',0)+1:]
    initial = {"title":title,"content":content}
    editForm = createPageForm(initial)
    return render(request,"encyclopedia/edit.html",{
        "form":editForm,
        "title" : title
    })

def randomPage(request):
    entries_list = util.list_entries()
    index = random.randint(0,len(entries_list)-1)
    title = entries_list[index]
    print(title)
    return redirect("entry",title = title)