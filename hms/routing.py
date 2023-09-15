from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/hms/hmsproduct/(?P<company_id>[\w-]+)/$", consumers.HMSProductConsumer.as_asgi()),
]