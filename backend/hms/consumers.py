import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from hms.models import HMSProduct


class HMSProductConsumer(WebsocketConsumer):
    def connect(self):
        self.user_company_id = self.scope["url_route"]["kwargs"]["company_id"]
        self.group_name = f"{self.user_company_id}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        # TODO: add user authentication and access level checks before accepting
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    # websocket received message from clients making change to hmsproduct
    def receive(self, text_data):
        message = "hmsproductupdated"

        # send message to websocket group that invokes the coresponding consumer method
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, 
            {
                "type": "hmsproduct.add.product", # the method invoked in member clients' consumer
                "message": message,
            }
        )

    # a client recieves message from group websocket
    def hmsproduct_add_product(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))