from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=20)
    def __str__(self):
        return self.category
    #def get_absolute_url(self):
    #    return reverse('cat-detail', kwargs={'pk': self.pk})



class Item(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,blank=False,on_delete=models.CASCADE)
    hsncode = models.IntegerField(blank=True)
    item_name = models.CharField(max_length=20,blank=False)
    gst = models.FloatField(max_length=2,blank=False)
    mrp = models.FloatField(max_length=15,blank=True)
    buy_price = models.FloatField(max_length=15,blank=True)
    sell_price = models.FloatField(max_length=15,blank=False)
    unit = models.CharField(max_length=10,blank=False)
    def __str__(self):
        return self.item_name

class Customer(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=40,blank=False)
    address = models.CharField(max_length=80,blank=False)
    state = models.CharField(max_length=20,blank=False)
    state_code = models.IntegerField(blank=False)
    gst_number = models.CharField(max_length=20,blank=True)
    def __str__(self):
        return self.name



class Profile(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=40,blank=False)
    firm_name = models.CharField(max_length=50,blank=False)
    firm_address = models.CharField(max_length=80,blank=False)
    mobile_number = models.IntegerField(blank=False)
    gst_number = models.CharField(max_length=20)
    pan_number = models.CharField(max_length=15)
    bank_account_number = models.IntegerField(blank=False)
    bank_name = models.CharField(max_length=25,blank=False)
    bank_ifsc_code = models.CharField(max_length=15,blank=False)
    bank_branch_address = models.CharField(max_length=80)

class CustomerInvoice(models.Model):
    invoice_no = models.IntegerField(blank=False,null=False)
    po_no = models.CharField(blank=True,max_length=10)
    date = models.DateField(auto_now=True)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,blank=False,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.invoice_no)
class Invoice(models.Model):
    sno = models.IntegerField(default=0)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    item_name = models.ForeignKey(Item,on_delete=models.CASCADE)
    invoice= models.ForeignKey(CustomerInvoice,on_delete=models.CASCADE,blank=False,null=False)
    rate = models.FloatField(max_length=15)
    quantity = models.IntegerField(default=1)
    discount = models.FloatField(max_length=3,default=0,blank=True)
