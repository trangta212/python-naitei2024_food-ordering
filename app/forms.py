from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django import forms

from app.constants import RATING_CHOICES
from app.models import Category, MenuItem, Review, User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].help_text = ''
        self.fields['email'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Username')})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Email')})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Password')})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Confirm Password')})

class LogInForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(LogInForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].help_text = ''
        self.fields['password'].help_text = ''

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Email')})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Password')})

class ReviewForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write a review"}))
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select())

    class Meta:
        model = Review
        fields = ['comment', 'rating']

class MenuItemForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'quantity', 'categories', 'image_url']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price must be greater than or equal to 0.")
        return price
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError("Quantity must be greater than or equal to 0.")
        return quantity
