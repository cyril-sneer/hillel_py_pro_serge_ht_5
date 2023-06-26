from math import hypot

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import TriangleForm


# Create your views here.
def calc_hypotenuse(request, hyp_c=None):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TriangleForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            lag_a = form.cleaned_data.get('leg_a')
            lag_b = form.cleaned_data.get('leg_b')
            hyp_c = f"{hypot(lag_a, lag_b):.2f}"

            # redirect to a new URL:
            return render(request, "catalog/input_triangle.html", {"form": form, "hyp_c": hyp_c})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TriangleForm()

    return render(request, "catalog/input_triangle.html", {"form": form})
