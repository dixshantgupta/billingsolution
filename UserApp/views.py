from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from UserApp.forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView,FormView)
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from . import forms
#**************************************************************************************************************************
class HomePageView(TemplateView):
    template_name = 'homepage.html'
#****************************************************************************************************************
class RegisterCreateView(CreateView,UserCreationForm):
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('UserApp:loginpage')
    #model = UserCreationFor
#***********************************************************************************************************************************
class LoginView(TemplateView):
    template_name = 'Loginpage.html'
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                current_user=request.user
                if models.Profile.objects.filter(username=current_user).exists():
                    return HttpResponseRedirect(reverse_lazy('UserApp:dashboard'))
                else:
                    return HttpResponseRedirect(reverse_lazy('UserApp:profile'))
            else:
                return HttpResponse("Inactive user.")
        else:
            return render(request,'Loginpage.html',context={'errorinject':'Invalid Username Or password Please Check Again'})
        return render(request, "homepage.html")
#*****************************************************************************************************************************************
class LogoutView(View,LoginRequiredMixin):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('homepage'))
#************************************************************************************************************************************
#*******************************************************************************************************************************
class DashboardView(LoginRequiredMixin,TemplateView):
    login_url = 'UserApp:loginpage'
    def get(self,request):
        current_user=request.user
        return render(request,'dashboard.html',context={'insert_user':current_user})
#****************************************************************************************************************

############################################### PROFILE ############################################################
class ProfileCreateView(LoginRequiredMixin,CreateView):
    login_url = 'UserApp:loginpage'
    template_name = 'UserApp/profile.html'
    success_url = reverse_lazy('UserApp:dashboard')
    model = models.Profile
    fields = ['name','firm_name','firm_address','mobile_number','gst_number','pan_number','bank_name','bank_account_number','bank_ifsc_code','bank_branch_address']
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)
class ProfileListView(LoginRequiredMixin,ListView):
    login_url = 'UserApp:loginpage'
    model=models.Profile
    template_name='UserApp/profile_list.html'
class ProfileUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = 'UserApp:loginpage'
    model = models.Profile
    fields = ['name','firm_name','firm_address','mobile_number','gst_number','pan_number','bank_name','bank_account_number','bank_ifsc_code','bank_branch_address']
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)
    def test_func(self):
        pro = self.get_object()
        if self.request.user == pro.username:
            return True
        return False
    template_name='UserApp/profile_update.html'
    success_url = reverse_lazy('UserApp:profile-list')
##################################################### CATEGORY ########################################################
class CategoryCreateView(LoginRequiredMixin,CreateView):
    login_url = 'UserApp:loginpage'
    template_name = 'UserApp/category_add.html'
    success_url = reverse_lazy('UserApp:cat-list')
    model = models.Category
    fields = ('category',)
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)
class CategoryListView(LoginRequiredMixin,ListView):
    login_url = 'UserApp:loginpage'
    model=models.Category
    template_name='UserApp/category_list.html'
class CategoryUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = 'UserApp:loginpage'
    model = models.Category
    fields = ['category',]
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)
    def test_func(self):
        cat = self.get_object()
        if self.request.user == cat.username:
            return True
        return False
    template_name='UserApp/category_form.html'
    success_url = reverse_lazy('UserApp:cat-list')
class CategoryDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = 'UserApp:loginpage'
    model = models.Category
    def test_func(self):
        cat = self.get_object()
        if self.request.user == cat.username:
            return True
        return False
    success_url = reverse_lazy("UserApp:cat-list")
    template_name = 'UserApp/category_delete.html'

############################################## ITEM  ################################################################################
class ItemCreateView(LoginRequiredMixin,CreateView):
    login_url = 'UserApp:loginpage'
    template_name = 'UserApp/item_add.html'
    success_url = reverse_lazy('UserApp:item-list')
    model = models.Item
    form_class= forms.ItemForm
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
class ItemListView(LoginRequiredMixin,ListView):
    login_url = 'UserApp:loginpage'
    model=models.Item
    template_name='UserApp/item_list.html'
class ItemUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = 'UserApp:loginpage'
    model = models.Item
    form_class = forms.ItemForm
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def test_func(self):
        item = self.get_object()
        if self.request.user == item.username:
            return True
        return False
    template_name='UserApp/item_form.html'
    success_url = reverse_lazy('UserApp:item-list')
class ItemDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = 'UserApp:loginpage'
    model = models.Item
    def test_func(self):
        item = self.get_object()
        if self.request.user == item.username:
            return True
        return False
    success_url = reverse_lazy("UserApp:item-list")
    template_name = 'UserApp/item_delete.html'

############################################## CUSTOMER  ################################################################################
class CustomerCreateView(LoginRequiredMixin,CreateView):
    login_url = 'UserApp:loginpage'
    template_name = 'UserApp/customer_add.html'
    success_url = reverse_lazy('UserApp:customer-list')
    model = models.Customer
    fields = ('name','address','state','state_code','gst_number')
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)
class CustomerListView(LoginRequiredMixin,ListView):
    login_url = 'UserApp:loginpage'
    model=models.Customer
    template_name='UserApp/customer_list.html'
class CustomerUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = 'UserApp:loginpage'
    model = models.Customer
    fields = ['name','address','state','state_code','gst_number']
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)
    def test_func(self):
        cust = self.get_object()
        if self.request.user == cust.username:
            return True
        return False
    template_name='UserApp/customer_form.html'
    success_url = reverse_lazy('UserApp:customer-list')
class CustomerDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = 'UserApp:loginpage'
    model = models.Customer
    def test_func(self):
        cust = self.get_object()
        if self.request.user == cust.username:
            return True
        return False
    success_url = reverse_lazy("UserApp:customer-list")
    template_name = 'UserApp/customer_delete.html'
#********************************************* Generate Bill **************************************************************
def load_item(request):
    category_id = request.GET.get('category')
    current_user=request.user
    items = models.Item.objects.filter(username= current_user,category_id=category_id).order_by('item_name')
    return render(request, 'UserApp/item_dropdown.html', {'items': items})

def load_rate(request):
    current_user=request.user
    item_id = request.GET.get('item')
    rate = models.Item.objects.values_list('sell_price', flat=True).get(pk=item_id)
    return render(request, 'UserApp/rate_dropdown.html', {'rate': rate})

@login_required
def create_invoice(request):
    invoice = models.CustomerInvoice.objects.filter(username=request.user).values_list('invoice_no', flat=True)
    if  not(invoice):
        invoice=1
    else:
        invoice =max(invoice)
        invoice = invoice + 1
    template_name = 'UserApp/genrate_invoice.html'
    if request.method == 'POST':
        sno = 1
        customer_form = forms.CustomerInvoiceForm(request.user,request.POST)
        formset = forms.InvoiceFormset(request.POST)
        if formset.is_valid() and customer_form.is_valid() :
            instance = customer_form.save(commit=False)
            instance.username = request.user
            instance.invoice_no = invoice
            for form in formset:
                current_user = request.user
                category = form.cleaned_data.get('category')
                item = form.cleaned_data.get('item_name')
                rate = form.cleaned_data.get('rate')
                quantity = form.cleaned_data.get('quantity')
                discount = form.cleaned_data.get('discount')
                if category and item and rate and quantity and sno<=10:
                    customer_form.save()
                    models.Invoice(invoice=instance,sno=sno,category=category,item_name=item,rate=rate,quantity=quantity,discount=discount,username=request.user).save()
                    sno = sno + 1
            return invoice_html(request,current_user,invoice)
        else:
            return HttpResponse('PLEASE FIILL ALL DETAILS PROPERLY EVEN FILL DISCOUNT 0')
    else:
        customer_form = forms.CustomerInvoiceForm(request.user)
        formset = forms.InvoiceFormset()
        for form in formset:
            form.fields['category'].queryset = models.Category.objects.filter(username=request.user).order_by('category')
            form.fields['item_name'].queryset = models.Item.objects.filter(username=request.user)
    return render(request, template_name, {
        'formset': formset,'invoice_no':invoice,'customer_form':customer_form,
    })


#######################################################################################################

def invoice_html(request,current_user,invoice):
    customer_id = max(models.CustomerInvoice.objects.filter(username=current_user,invoice_no=invoice).values_list('customer', flat=True))
    po_no = max(models.CustomerInvoice.objects.filter(username=current_user,invoice_no=invoice).values_list('po_no', flat=True))
    date = max(models.CustomerInvoice.objects.filter(username=current_user,invoice_no=invoice).values_list('date', flat=True))
    id_invoice = max(models.CustomerInvoice.objects.filter(username=current_user,invoice_no=invoice).values_list('id', flat=True))
    customer = max(models.Customer.objects.filter(username=current_user,id = customer_id).values_list('name', flat=True))
    address = max(models.Customer.objects.filter(username=current_user,id = customer_id).values_list('address', flat=True))
    state = max(models.Customer.objects.filter(username=current_user,id = customer_id).values_list('state', flat=True))
    state_code = max(models.Customer.objects.filter(username=current_user,id = customer_id).values_list('state_code', flat=True))
    gst_number = max(models.Customer.objects.filter(username=current_user,id = customer_id).values_list('gst_number', flat=True))
    ######################item#######################
    item_id = models.Invoice.objects.filter(username=current_user,invoice=id_invoice).values_list('item_name', flat=True)
    sno = models.Invoice.objects.filter(username=current_user,invoice=id_invoice).values_list('sno', flat=True)
    rate = models.Invoice.objects.filter(username=current_user,invoice=id_invoice).values_list('rate', flat=True)
    qty = models.Invoice.objects.filter(username=current_user,invoice=id_invoice).values_list('quantity', flat=True)
    discount = models.Invoice.objects.filter(username=current_user,invoice=id_invoice).values_list('discount', flat=True)
    ##################################################item#################################
    hsn = []
    item_name =[]
    gst = []
    unit = []
    for j in sno:
        hsn.append(models.Item.objects.filter(username=current_user,id=item_id[j-1]).values_list('hsncode', flat=True))
        item_name.append (models.Item.objects.filter(username=current_user,id=item_id[j-1]).values_list('item_name', flat=True))
        gst.append(models.Item.objects.filter(username=current_user,id=item_id[j-1]).values_list('gst', flat=True))
        unit.append( models.Item.objects.filter(username=current_user,id=item_id[j-1]).values_list('unit', flat=True))
    #############################################profile###############################
    firm_name = models.Profile.objects.filter(username=current_user).values_list('firm_name', flat=True)
    firm_address = models.Profile.objects.filter(username=current_user).values_list('firm_address', flat=True)
    mobile_number = models.Profile.objects.filter(username=current_user).values_list('mobile_number', flat=True)
    gst_number_user = models.Profile.objects.filter(username=current_user).values_list('gst_number', flat=True)
    bank_account_number = models.Profile.objects.filter(username=current_user).values_list('bank_account_number', flat=True)
    bank_name = models.Profile.objects.filter(username=current_user).values_list('bank_name', flat=True)
    bank_ifsc_code = models.Profile.objects.filter(username=current_user).values_list('bank_ifsc_code', flat=True)
    bank_branch_address = models.Profile.objects.filter(username=current_user).values_list('bank_branch_address', flat=True)
    email = models.User.objects.filter(username=current_user).values_list('email', flat=True)
    data = {'firm_name':firm_name[0],'firm_address':firm_address[0],'mobile_number':mobile_number[0],'email':email[0],
    'gst_number_user':gst_number_user[0],'bank_account_number':bank_account_number[0],'bank_name':bank_name[0],
    'bank_ifsc_code':bank_ifsc_code[0],'bank_branch_address':bank_branch_address[0],'invoice':invoice,'date':date,
    'customer':customer,'address':address,'state':state,'state_code':state_code,'gst_number':gst_number,
    'total_qty':sum(qty)}
    for i in sno:
        key = 'sno{}'.format(i)
        data[key]=sno[i-1]
        key = 'item_name{}'.format(i)
        data[key]=item_name[i-1][0]
        key = 'hsn{}'.format(i)
        data[key]=hsn[i-1][0]
        key = 'qty{}'.format(i)
        data[key]=qty[i-1]
        key = 'unit{}'.format(i)
        data[key]=unit[i-1][0]
        key = 'rate{}'.format(i)
        data[key]=rate[i-1]
        key = 'discount{}'.format(i)
        data[key]=discount[i-1]
        key = 'ammount{}'.format(i)
        data[key]=round((qty[i-1]*rate[i-1])-((discount[i-1]*(qty[i-1]*rate[i-1]))/100),2)
        key = 'cgst{}'.format(i)
        data[key]=(gst[i-1][0])/2
        key = 'sgst{}'.format(i)
        data[key]=(gst[i-1][0])/2
        key = 'cgst_rate{}'.format(i)
        data[key]=round(((data['ammount{}'.format(i)])*((gst[i-1][0])/2))/100,2)
        key = 'sgst_rate{}'.format(i)
        data[key]=round(((data['ammount{}'.format(i)])*((gst[i-1][0])/2))/100,2)
        key = 'total{}'.format(i)
        ans = (data['ammount{}'.format(i)]) + 2*(((data['ammount{}'.format(i)])*((gst[i-1][0])/2))/100)
        data[key]=str(round(ans, 2))
    sum1=0
    sum2=0
    sum3=0
    for z in sno:
        key = 'ammount{}'.format(z)
        sum1 = data[key] + sum1
        key1 = 'cgst_rate{}'.format(z)
        sum2 = data[key1] + sum2
        key2 = 'total{}'.format(z)
        sum3 = float(data[key2])+ sum3
    data['total_rate']=round(sum1,2)
    data['total_gst_rate']=sum2
    data['total_total']=round(sum3,2)
    data['total_round']=str(round(sum3))
    num_to_word=int_to_en(int(round(sum3)))
    data['num_to_word']  = num_to_word
    if state_code == int(gst_number_user[0][1:2]):
        #return render(request, "UserApp/interstate-gst.html",data)
        pdf = render_to_pdf('UserApp/interstate.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        for a in sno:
            key = 'cgst{}'.format(a)
            data[key]=(gst[a-1][0])
            key = 'cgst_rate{}'.format(a)
            data[key]=round(((data['ammount{}'.format(a)])*(gst[a-1][0]))/100,2)
            key = 'sgst_rate{}'.format(a)
        data['total_gst_rate'] = round(2*data['total_gst_rate'],2)
        pdf = render_to_pdf('UserApp/intrastate.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
        #html_string = render_to_string("UserApp/intrastate-gst.html",data)
        #return html_to_pdf_view(request,html_string)
##################################################number to words##################################33333

def int_to_en(num):
    d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',19: 'nineteen', 20 : 'twenty',30 : 'thirty', 40 : 'forty', 50 : 'fifty', 60 : 'sixty',70 : 'seventy', 80 : 'eighty', 90 : 'ninety' }
    k = 1000
    m = k * 100
    b = m * 100
    assert(0 <= num)
    if (num < 20):
        return d[num]
    if (num < 100):
        if num % 10 == 0: return d[num]
        else: return d[num // 10 * 10] + '-' + d[num % 10]
    if (num < k):
        if num % 100 == 0: return d[num // 100] + ' hundred'
        else: return d[num // 100] + ' hundred ' + int_to_en(num % 100)
    if (num < m):
        if num % k == 0: return int_to_en(num // k) + ' thousand'
        else: return int_to_en(num // k) + ' thousand, ' + int_to_en(num % k)
    if (num < b):
        if (num % m) == 0: return int_to_en(num // m) + ' lakh'
        else: return int_to_en(num // m) + ' lakh, ' + int_to_en(num % m)
    raise AssertionError('num is too large: %s' % str(num))
#########################view##################################################3
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from UserApp.utils import render_to_pdf #created in step 4
from django.template.loader import get_template
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
             'today': '02-04-2019',
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
"""class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template('invoice.html')
        context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
        }
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")"""




class CustomerInvoiceListView(LoginRequiredMixin,ListView):
    login_url = 'UserApp:loginpage'
    model=models.CustomerInvoice
    template_name='UserApp/customerinvoice_list.html'
class CustomerInvoiceUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = 'UserApp:loginpage'
    model = models.CustomerInvoice
    fields = ['customer','po_no']
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)
    def test_func(self):
        cust = self.get_object()
        if self.request.user == cust.username:
            return True
        return False
    template_name='UserApp/customerinvoice_update.html'
    success_url = reverse_lazy('UserApp:customerinvoice-list')
class InvoiceDetailView(LoginRequiredMixin,DetailView):
    login_url = 'UserApp:loginpage'
    context_object_name = 'invoice_details'
    queryset = models.Invoice.objects.all()
    slug_field = "invoice"
    sluge_url_kwarg = "invoice"
    model=models.Invoice
    #lookup_field = "invoice"
    template_name='UserApp/invoice_list.html'


###############################################33pdf#########################################
