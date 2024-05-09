from django.urls import path
from .views import *

app_name = 'purchase'
urlpatterns = [
    path('', PurchaseListCreateApiView.as_view(), name='ListCreate'),
    path('<str:po_number>/', PurchaseUpdatedeleteView.as_view(), name='UpdateDelete'),
    path('<str:po_number>/acknowledge/',
         AcknowledgeApi.as_view(), name='Acknowledge'),
    path('<str:po_number>/delivery/', DeliveryApi.as_view(), name='Delivery'),
    path('<str:po_number>/rating/', RatingApi.as_view(), name='Rating'),
]
