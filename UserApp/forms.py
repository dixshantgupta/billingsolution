from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models
from django.forms import (formset_factory, modelformset_factory)
class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class ItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ['category','hsncode','item_name','gst','mrp','buy_price','sell_price','unit']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        cat_of_current_user = models.Category.objects.filter(username=user).values('category')
        # restrict the queryset of 'current_user category'
        self.fields['category'].queryset = self.fields['category'].queryset.filter(category__in=cat_of_current_user)

class CustomerInvoiceForm(forms.ModelForm):
    class Meta:
        model = models.CustomerInvoice
        fields = ['customer','po_no']
    def __init__(self, user, *args, **kwargs):
        super(CustomerInvoiceForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = models.Customer.objects.filter(username=user)

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = models.Invoice
        fields = ['category','item_name','rate','quantity','discount']
    #def __init__(self, user, *args, **kwargs):
    #    super(InvoiceForm, self).__init__(*args, **kwargs)
    #    self.fields['category'].queryset = models.Category.objects.filter(username=user)
    #    self.fields['item_name'].queryset = models.Item.objects.filter(username=user)



InvoiceFormset = formset_factory(InvoiceForm)
InvoiceModelFormset = modelformset_factory(
    models.Invoice,
    fields=('category','item_name','rate','quantity','discount',),
    extra=1,
        )

#CustomerFormset = modelformset_factory(
#    models.CustomerInvoice,
#    fields=('customer','po_no',),
#    extra=1,
#)
