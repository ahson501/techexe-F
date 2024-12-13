from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search Plants', max_length=100)
