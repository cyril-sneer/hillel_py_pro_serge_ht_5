from math import hypot

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import TriangleForm, PersonModelForm
from .models import Person


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


def create_person(request):
    if request.method == "POST":
        form = PersonModelForm(request.POST)

        if form.is_valid():
            person = form.save()
            return redirect(person.get_absolute_url())

    else:
        form = PersonModelForm()
    return render(request, 'catalog/person_form.html', {'form': form})


def update_person(request, pk):
    person = get_object_or_404(Person, pk=pk)

    if request.method == "POST":
        form = PersonModelForm(request.POST, instance=person)

        if form.is_valid():
            person = form.save()

            if 'Update_button' in request.POST:
                messages.success(request, "Person profile updated!")
                return redirect(person.get_absolute_url())

            elif 'Delete_button' in request.POST:
                person.delete()
                messages.success(request, "Person profile DELETED!")
                return redirect(reverse("catalog:person"))

    else:
        form = PersonModelForm(instance=person)
    return render(request, 'catalog/person_form.html', {'form': form, "person": person})
