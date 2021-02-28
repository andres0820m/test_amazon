from django.shortcuts import render
from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Profile, Code
from api.serializers import UserSerializer, CodeSerializer
from api.amazon_wrapped import AmazonWrapped
from api.exceptions import *


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['head', 'post']


class RedeemCode(APIView):

    def post(self, request):
        amazon = AmazonWrapped()
        try:
            email = request.data['email']
            code = request.data['code']
            user = Profile.objects.filter(email=email).first()
        except ApiKeyError:
            amazon.web_driver.close()
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if user is not None:
            # try:
            amazon.login(email=user.email, password=user.password)
            amazon.move_to_cards()
            amazon.check_cards_balance()
            old_value = amazon.get_actual_balance()
            amazon.redeem_card(code)
            sta, val = amazon.check_if_redeem()
            print(sta, val, old_value)
            if sta:
                code = Code(user=user, code=code, balance_before=old_value,
                            balance_after=val, status="Done")
                code.save()

            else:
                code = Code(user=user, code=code, balance_before=old_value,
                            balance_after=old_value, status="Fail")
                code.save()

            # except:
            # return Response("wrong password", status=status.HTTP_400_BAD_REQUEST)
            amazon.web_driver.close()
            return Response(val, status=status.HTTP_200_OK)
        else:
            amazon.web_driver.close()
            return Response(status=status.HTTP_404_NOT_FOUND)


class CodeViewSet(viewsets.ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer
    http_method_names = ['head', 'get']


class CodeApiView(APIView):
    def get(self, request):
        try:
            email = request.data['email']
            user = Profile.objects.filter(email=email).first()
        except ApiKeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if user is not None:
            codes = Code.objects.all().filter(user=user).values()
            return Response(codes, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_404_NOT_FOUND)
