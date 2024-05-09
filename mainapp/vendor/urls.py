from django.urls import path
from .views import *

app_name = 'vendor'
urlpatterns = [
    path('', VendorsListCreateApiView.as_view(), name='ListCreate'),
    path('<str:vendor_code>/', VendorUpdatedeleteView.as_view(), name='UpdateDelete'),
    path('<str:po_number>/orederdate/', OrderApi.as_view(), name='Order'),
    path('<str:vendor_code>/performance/',
         PerformanceApi.as_view(), name='Performance'),
]
