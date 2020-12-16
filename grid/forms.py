from django import forms

from .models import Products


class ProductsForm(forms.Form):
    """
    Products ModelForm used in add.html
    """

    product = forms.ModelMultipleChoiceField(
        queryset=Products.objects.all(), widget=forms.CheckboxSelectMultiple
    )
