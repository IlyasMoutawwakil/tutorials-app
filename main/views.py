# render ...renders... an HTML page
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Tutorial, TutorialSeries, TutorialCategory
from .forms import NewUserForm


def single_slug(request, single_slug):
    # loop through TutorialCategory objects so we can match slugs
    categories = [c.category_slug for c in TutorialCategory.objects.all()]

    if single_slug in categories:
        # find matching series by matching slugs
        # __ after a forieng key points to an attribute of that foriegn key
        matching_series = TutorialSeries.objects.filter(
            tutorial_category__category_slug=single_slug)

        series_urls = {}
        for m in matching_series.all():
            # .earliest() can be used since we used DateTime field
            part_one = Tutorial.objects.filter(
                tutorial_series__tutorial_series=m.tutorial_series).earliest("tutorial_published")
            print(matching_series.all())
            print()
            series_urls[m] = part_one.tutorial_slug
        print(series_urls)
        return render(request,
                      "main/category.html",
                      {"part_ones": series_urls})

    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
    if single_slug in tutorials:
        this_tutorial = Tutorial.objects.get(tutorial_slug=single_slug)

        # Create sidebar showing series
        # get tutorials in same series as this_tutorial
        tutorials_from_series = Tutorial.objects.filter(
            tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by("tutorial_published")

        # convert to list to get index of this_tutorial
        this_tutorial_idx = list(tutorials_from_series).index(this_tutorial)

        return render(request,
                      "main/tutorial.html",
                      {"tutorial": this_tutorial,
                       "sidebar": tutorials_from_series,
                       "this_tutorial_idx": this_tutorial_idx})

    return HttpResponse(f"{single_slug} doesn't correspond to anything")


# HttpResponse lets us respond to requests with html
# def homepage(request):
#     return render(request=request,
#                   template_name="main/home.html",
#                   context={"tutorials": Tutorial.objects.all}
#                   )
# HttpResponse lets us respond to requests with html
def homepage(request):
    return render(request=request,
                  template_name="main/categories.html",
                  # context allows us to pass things to be rendered
                  # in this case we're passing objets from a model
                  context={"categories": TutorialCategory.objects.all()}
                  )


def register(request):
    # request by default is only GET. Must specify a POST request
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            # save user
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            messages.info(request, f"You are now logged in as {username}")
            # automatically log the user in
            login(request, user)
            # can redirect to <app_name>:<url>  or a path (like "/")
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: form.error_messages[msg]")

    form = NewUserForm
    return render(request,
                  "main/register.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("main:homepage")


def login_request(request):
    # request by default is only GET. Must specify a POST request
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("main:homepage")
            else:
                messages.error(request, f"Invalid username or password")
                return redirect("main:homepage")
        else:
            messages.error(request, f"Invalid username or password")
            return redirect("main:homepage")

    form = AuthenticationForm()
    return render(request,
                  "main/login.html",
                  {"form": form})
