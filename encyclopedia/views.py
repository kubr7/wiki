from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown
import random
from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    try:
        if not content:
            return None
        else:
            return markdowner.convert(content)
    except Exception as e:
        # Handle the exception (e.g., log the error)
        return None

def index(request):
    site_name = "Encyclopedia"

    entries = util.list_entries()
    return render(
        request, "encyclopedia/index.html", {"site_name": site_name, "entries": entries}
    )

def entry(request, title):
    site_name = "Encyclopedia"
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(
            request,
            "encyclopedia/error.html",
            {"site_name": site_name, "message": "This entry does not exist"},
        )
    else:
        return render(
            request,
            "encyclopedia/entry.html",
            {"site_name": site_name, "title": title, "content": html_content},
        )

def search(request):
    site_name = "Encyclopedia"

    if request.method == "POST":
        entry_search = request.POST.get("q", "").strip()

        if not entry_search:
            # If no search term is provided, render search.html with an error message
            return render(
                request,
                "encyclopedia/error.html",
                {
                    "site_name": site_name,
                    "message": "Please enter a valid search term."
                },
            )

        # Attempt to convert Markdown to HTML for the searched entry
        html_content = convert_md_to_html(entry_search)

        if html_content is not None:
            # If content found, render entry.html with the entry details
            return render(
                request,
                "encyclopedia/entry.html",
                {
                    "site_name": site_name,
                    "title": entry_search,
                    "content": html_content,
                },
            )
        else:
            # If content not found, suggest similar entries
            all_entries = util.list_entries()
            recommendation = [
                entry for entry in all_entries if entry_search.lower() in entry.lower()
            ]

            if recommendation:
                # If there are similar entries, render search.html with recommendations
                return render(
                    request,
                    "encyclopedia/search.html",
                    {"site_name": site_name, "recommendation": recommendation},
                )
            else:
                # If no similar entries found, render error.html
                return render(
                    request,
                    "encyclopedia/error.html",
                    {
                        "site_name": site_name,
                        "message": "This entry does not exist!",
                    },
                )
    else:
        # If request method is not POST, render search.html with no recommendations
        return render(request, "encyclopedia/search.html", {"site_name": site_name})

def new_page(request):
    site_name = "Encyclopedia"
    if request.method == "GET":
        return render(
            request,
            "encyclopedia/new.html",
            {
                "site_name": site_name,
            },
        )
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        titleExist = util.get_entry(title)
        if not title or not content:
            return render(
                request,
                "encyclopedia/error.html",
                {
                    "site_name": site_name,
                    "message": "Please enter both title and description!",
                },
            )
        elif titleExist is not None:
            return render(
                request,
                "encyclopedia/error.html",
                {"site_name": site_name, "message": "Page already exists!"},
            )
        else:
            util.save_entry(title, content)
            entries = util.list_entries()
            html_content = convert_md_to_html(title)
            return render(
                request,
                "encyclopedia/index.html",
                {"site_name": site_name, "entries": entries, "content": html_content},
            )

def edit(request):
    site_name = "Encyclopedia"
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(
            request,
            "encyclopedia/edit.html",
            {"site_name": site_name, "title": title, "content": content},
        )

def save_edit(request):
    site_name = "Encyclopedia"
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        return render(
            request,
            "encyclopedia/entry.html",
            {"site_name": site_name, "title": title, "content": html_content},
        )

def delete_page(request, title):
    site_name = "Encyclopedia"

    if request.method == "POST":
        util.delete_entry(title)
        return HttpResponseRedirect(
            reverse("index")
        )  # Redirect to the index page after deletion

    return render(
        request,
        "encyclopedia/delete.html",
        {
            "site_name": site_name,
            "title": title,
        },
    )

def random_page(request):
    site_name = "Encyclopedia"
    # Get all entries
    all_entries = util.list_entries()

    if not all_entries:
        # Handle the case when there are no entries
        return render(request, "encyclopedia/empty.html")

    # Select a random entry
    random_entry = random.choice(all_entries)

    # Convert Markdown to HTML
    html_content = util.convert_md_to_html(random_entry)

    # Render the template with the random entry's title and content
    return render(
        request,
        "encyclopedia/entry.html",
        {"site_name": site_name, "title": random_entry, "content": html_content},
    )
