from django import forms


class SortForm(forms.Form):
    SORT_CHOICES = (
        ('sale_price', 'Sort by price: low to high'),
        ('-sale_price', 'Sort by price: high to low'),
        ('-created', 'Sort by new'),
    )

    field = forms.ChoiceField(choices=SORT_CHOICES)
