from django.shortcuts import render
from django.views import  View
from django.views.generic import  TemplateView
from django.http import HttpResponseBadRequest, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import africastalking


@method_decorator(csrf_exempt, name='dispatch')
class SMSRequest(View):
    def __init__(self):
        super(SMSRequest, self).__init__()
        self.username = "sandbox"
        self.api_key = ""
        africastalking.initialize(self.username, self.api_key)
        self.sms = africastalking.SMS
        self.clients = []
        self.shortCode = ""


    def fetch_sms_sync(self):

        try:
            last_received_id = 0
           
            MessageData = self.sms.fetch_messages(last_received_id)
            messages = MessageData['SMSMessageData']['Messages']
            # Get client Number
            client = messages[0]["from"]
            return client
            
        except Exception as e:
            print ('Encountered an error while fetching: %s' % str(e))

    def send_sms_sender_id(self, recipients):
        message = "I'm a lumberjack and it's ok, I sleep all night and I work all day"
        sender = self.shortCode
        try:
            responses = self.sms.send(message, recipients, sender)
            status = responses["SMSMessageData"]["Recipients"][0]
            return status
    
        except Exception as e:
            print('Encountered an error while sending: %s client - %s' % (str(e), str(recipients)))

    def get(self, request):
        return  HttpResponseBadRequest("<h1> Bad Request </h1>", status=400)
    
  
    def post(self, request):
   
        try:
            # Receive messages
            self.clients.append(self.fetch_sms_sync())
            # Send Response
            responses = self.send_sms_sender_id(self.clients)
            context = {"Status": responses, "Clients": self.clients}
            return render(request, template_name="SMSRequest.html", context=context)
        except:
            return HttpResponseBadRequest("<h1> Bad Request </h1>", status=400)

    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)    
