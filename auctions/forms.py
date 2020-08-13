from auctions.models import Category
from django import forms
import datetime

class BidForm(forms.Form):
    bid = forms.DecimalField(label='bid')


class CreateListingForm(forms.Form):
    title = forms.CharField(label='title')
    description = forms.CharField(widget=forms.Textarea, label='description')
    image = forms.ImageField(label='image')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='category')
    valid_until = forms.DateField(label='valid until', widget=forms.SelectDateWidget, initial=datetime.date.today)
    price = forms.DecimalField(label='price', min_value = 0.1)
