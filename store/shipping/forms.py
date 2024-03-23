from django import forms

from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


from .models import Shipping, Address


class ShppingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ('delivery_date', 'delivery_time_slot', 'address',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['delivery_date'] = JalaliDateField(
            label='date',
            widget=AdminJalaliDateWidget()
        )
        self.fields['address'].queryset = Address.objects.filter(user=user)
        self.fields['address'].required = False


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address', 'city', 'province', 'building_number',
                  'unit', 'postal_code', 'receiver_first_name',
                  'receiver_last_name', 'mobile',)
