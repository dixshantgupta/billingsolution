from django.contrib import admin
from UserApp.models import Category,Item,Customer,Profile,CustomerInvoice,Invoice
# Register your models here.
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Customer)
admin.site.register(Profile)
admin.site.register(CustomerInvoice)
admin.site.register(Invoice)
