from django import forms


class TriangleForm(forms.Form):
    leg_a = forms.IntegerField(label="Катет A, см", required=True, min_value=1)
    leg_b = forms.IntegerField(label="Катет B, см", required=True, min_value=1)
