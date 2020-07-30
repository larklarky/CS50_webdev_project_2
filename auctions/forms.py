from django import forms

class BidForm(forms.Form):
    bid = forms.DecimalField(label='bid')