from django.urls import path
from .views import (
    create_restaurant,
    get_restaurants,
    create_ticket,
    update_ticket,
    get_tickets,
    buy_ticket,
    get_single_ticket,
    get_single_restaurant,
    PurchaseTicketsView
)

urlpatterns = [
    path('', get_restaurants),
    path('create/', create_restaurant),
    path('<restaurant_id>/', get_single_restaurant),
    path('ticket/<restaurant_id>/', get_tickets),
    path('ticket/single/<ticket_id>/', get_single_ticket),
    path('ticket/create/<restaurant_id>/', create_ticket),
    path('ticket/edit/<ticket_id>/', update_ticket),
    path('ticket/buy/<ticket_id>/', buy_ticket),
    path('purchase/tickets/', PurchaseTicketsView.as_view({'get':'list'}))
]
