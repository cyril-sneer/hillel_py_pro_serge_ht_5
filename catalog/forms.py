from django import forms

from catalog.models import Person


class TriangleForm(forms.Form):
    leg_a = forms.IntegerField(label="Катет A, см", required=True, min_value=1)
    leg_b = forms.IntegerField(label="Катет B, см", required=True, min_value=1)


class PersonModelForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["first_name", "last_name", "email"]
