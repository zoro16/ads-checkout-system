from django.conf.urls import url
from ads import views

urlpatterns = [
    url(r'^order/',
        views.OrderView.as_view(),
        name='order-list',
    ),
]
