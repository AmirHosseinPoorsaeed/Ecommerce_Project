from django import forms
from django.utils.translation import gettext_lazy as _


class SortForm(forms.Form):
    SORT_CHOICES = (
        ('sale_price', _('Sort by price: low to high')),
        ('-sale_price', _('Sort by price: high to low')),
        ('-created', _('Sort by new')),
    )

    field = forms.ChoiceField(choices=SORT_CHOICES, label=_('field'))
