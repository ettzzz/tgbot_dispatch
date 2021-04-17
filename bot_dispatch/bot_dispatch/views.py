# -*- coding: utf-8 -*-


from rest_framework.views import APIView
from rest_framework.response import Response

from tg_operator.messager import send_message

class botMessageSender(APIView):
    def post(self, request):
        receiver = request.data['to']
        link = request.data['link']
        text = request.data['text']
        status_code = send_message(receiver, link, text)
        
        if status_code == 200:
            res = {'msg': 'message sent!'}
        elif status_code == -1:
            res = {'msg': 'receiver not in the roster!'}
        else:
            res = {'msg': 'Failed!'}
        
        return Response(res)

