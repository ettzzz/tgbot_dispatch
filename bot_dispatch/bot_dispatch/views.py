# -*- coding: utf-8 -*-

import os

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from tg_operator.messager import send_message
from tg_operator.receptionist import we_are_open
from tg_operator.static_vars import ROOT

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


class latestV2raySubscription(APIView):
    def get(self, request):
        with open(os.path.join(ROOT, 'barnhouse', 'latest_v2ray.txt'), 'r') as f:
            res = f.read()
        return HttpResponse(res)


we_are_open()
