# Logic to send real time updates of orders to the Kitchen Display
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder
from restaurant.models import Order

class KitchenOrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.zone_id = self.scope["url_route"]["kwargs"]["zoneID"]
        self.room_group_name = f"kitchen_zone_{self.zone_id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "order_update", "data": data}
        )

    async def order_update(self, event):
        await self.send(text_data=json.dumps(event["data"], cls=DjangoJSONEncoder))
