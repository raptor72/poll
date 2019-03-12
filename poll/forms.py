from django import forms

class SomeForm(forms.Form):
    title = forms.CharField(max_length=50)
