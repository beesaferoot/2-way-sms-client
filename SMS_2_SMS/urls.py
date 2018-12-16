
# url for SMS_2_SMS

from django.urls import path
from .views import SMSRequest
app_name = "SMS_2_SMS"
urlpatterns = [
    path('^$', SMSRequest.as_view())
]