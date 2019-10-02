from django.urls import path,reverse
from UserApp import views
app_name = 'UserApp'
urlpatterns = [
    path('register/',views.RegisterCreateView.as_view(),name='register'),
    path('loginpage/',views.LoginView.as_view(),name='loginpage'),
    path('logout/',views.LogoutView.as_view(),name='logoutpage'),
    path('dashboard/',views.DashboardView.as_view(),name='dashboard'),
################################# PROFILE PATH ########################################################################
    path('profile/',views.ProfileCreateView.as_view(),name='profile'),
    path('profile_detail/',views.ProfileListView.as_view(),name='profile-list'),
    path('profile_update/<int:pk>/',views.ProfileUpdateView.as_view(), name='profile-update'),
################################CATEGORY PATH ##########################################################################
    path('add_category/',views.CategoryCreateView.as_view(),name='cat-add'),
    path('category/',views.CategoryListView.as_view(),name='cat-list'),
    path('category/<int:pk>/update/',views.CategoryUpdateView.as_view(), name='catinfo-update'),
    path('category/delete/<int:pk>/',views.CategoryDeleteView.as_view(),name='catinfo-delete'),
##################################ITEM PATH ############################################################################
    path('add_item/',views.ItemCreateView.as_view(),name='item-add'),
    path('item/',views.ItemListView.as_view(),name='item-list'),
    path('item/<int:pk>/update_item/',views.ItemUpdateView.as_view(), name='iteminfo-update'),
    path('item/delete/<int:pk>/',views.ItemDeleteView.as_view(),name='iteminfo-delete'),
##################################CUSTOMER PATH ############################################################################
    path('customer_item/',views.CustomerCreateView.as_view(),name='customer-add'),
    path('customer/',views.CustomerListView.as_view(),name='customer-list'),
    path('customer/<int:pk>/update_customer/',views.CustomerUpdateView.as_view(), name='customerinfo-update'),
    path('customer/delete/<int:pk>/',views.CustomerDeleteView.as_view(),name='customerinfo-delete'),
##########################################GENERATE BILL PATH #########################################################
   path('generate/ajax/load-item/', views.load_item, name='ajax_load_item'),
   path('generate/ajax/load-rate/', views.load_rate, name='ajax_load_rate'),
   path('generate', views.create_invoice, name='create_invoice'),
   path('invoice/',views.CustomerInvoiceListView.as_view(),name='customerinvoice-list'),
   path('customer/<int:pk>/update_invoice/',views.CustomerInvoiceUpdateView.as_view(), name='customerinvoice-update'),
   path('invoice/<int:slug>/item/',views.InvoiceDetailView.as_view(),name='invoice-list'),
 #  path('csgst-invoice/',views.pdf_date,name='invoice')
]
