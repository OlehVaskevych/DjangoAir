from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.user = self.scope["user"]
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": event["type"],
            "message": event["message"],
        }))


class PassengerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.passenger_group = f"passenger_{self.scope['url_route']['kwargs']['flight_id']}"
        await self.channel_layer.group_add(self.passenger_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.passenger_group, self.channel_name)

    async def flight_update(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
