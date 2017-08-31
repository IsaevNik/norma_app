import logging

from django.shortcuts import redirect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, StaticHTMLRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import PromoCode, Order
from core.serializers import GuestSerializer, OrderSerializer
from core.utils import payment_facade


logger = logging.getLogger('payment')


class CheckPromoCodeView(APIView):
    renderer_classes = (JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def get(request, *args, **kwargs):
        promo_code_name = request.GET.get('promo_code')
        if PromoCode.objects.filter(name=promo_code_name).exists():
            return Response({'exist': True})
        return Response({'exist': False})


class CreateGuestView(CreateAPIView):
    renderer_classes = (JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = GuestSerializer


class CreateOrderView(CreateAPIView):
    renderer_classes = (JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PaymentProcess(APIView):
    renderer_classes = (StaticHTMLRenderer,)
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, _args, **kwargs):
        logger.info(request.GET)
        order_id = payment_facade.check_sign(request.GET)
        if order_id:
            try:
                order = Order.accept_order(request.GET)
            except Order.DoesNotExist:
                logger.error('Order does not exist')
        else:
            logger.error('Sign checking fail')
        return Response()


class PaymentRedirectView(APIView):
    renderer_classes = (TemplateHTMLRenderer, )
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        return redirect('https://www.facebook.com/events/1945012882434130')


class IndexView(APIView):
    renderer_classes = (TemplateHTMLRenderer, )
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        return redirect('https://www.facebook.com/events/1945012882434130')