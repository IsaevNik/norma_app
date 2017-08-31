from django.http import Http404
from rest_framework import serializers
from django.conf import settings

from core.models import Guest, PromoCode, Order
from core.utils import payment_facade


class GuestSerializer(serializers.ModelSerializer):

    code = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = Guest
        fields = ('id', 'chat_id', 'code', 'name', 'count')

    def validate(self, attrs):
        if 'code' in attrs:
            promo_code = PromoCode.objects.filter(name=attrs.pop('code')).first()
            if not promo_code:
                raise Http404
            attrs['promo_code'] = promo_code
        return attrs


class OrderSerializer(serializers.ModelSerializer):

    link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ('guest', 'link')
        extra_kwargs = {
            'guest': {'write_only': True}
        }

    def validate(self, attrs):
        guest = attrs['guest']
        if guest.promo_code:
            attrs['amount'] = settings.WITH_CODE_COST * guest.count
        else:
            attrs['amount'] = settings.WITHOUT_CODE_COST * guest.count
        return attrs

    def get_link(self, obj):
        return payment_facade.get_terminal(obj.amount, obj.id)
