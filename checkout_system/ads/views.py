from django.views.generic import ListView
from ads.models import Order


class OrderView(ListView):
    template_name = 'ads/orders.html'
    model = Order
