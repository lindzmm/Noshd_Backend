from django import forms
from .models import RestaurantPost


class RestaurantPostForm(forms.ModelForm):
    class Meta:
        model = RestaurantPost
        fields = [
            'user',
            'establishment_name',
            'pub_date'
        ]
