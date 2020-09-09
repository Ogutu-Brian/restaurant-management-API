from django.urls import path
from .views import (
    PurchaseTicketsView,
    RestaurantView,
    TicketView,
)

urlpatterns = [
    path('', RestaurantView.as_view({'get': 'list'})),
    path('create/', RestaurantView.as_view({'post': 'create'})),
    path('<restaurant_id>/', RestaurantView.as_view({'get': 'retrieve'})),
    path('ticket/<restaurant_id>/', TicketView.as_view({'get':'list'})),
    path('ticket/single/<ticket_id>/',TicketView.as_view({'get':'retrieve'})),
    path('ticket/create/<restaurant_id>/',
         TicketView.as_view({'post': 'create'})),
    path('ticket/edit/<ticket_id>/', TicketView.as_view({'put':'update'})),
    path('purchase/tickets/', PurchaseTicketsView.as_view({'get': 'list'})),
    path('ticket/buy/<ticket_id>/',
         PurchaseTicketsView.as_view({'put': 'update'})),
]
