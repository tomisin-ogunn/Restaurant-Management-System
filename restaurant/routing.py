#Routes the websocket real time updates of orders

from django.urls import re_path
from restaurant.consumers import KitchenOrderConsumer

websocket_urlpatterns = [
    re_path(r"ws/kitchen-zone/(?P<zoneID>\d+)/$", KitchenOrderConsumer.as_asgi()),
]