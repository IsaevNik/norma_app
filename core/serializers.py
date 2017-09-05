from django.http import Http404
from rest_framework import serializers
from django.conf import settings

from core.exceptions import PromoterInactive
from core.models import Guest, PromoCode, Order, Promoter
from core.utils import payment_facade


__all__ = ['GuestSerializer', 'OrderSerializer', 'PromoterSerializer']


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

    def create(self, validated_data):
        guest = Guest.objects.filter(chat_id=validated_data.get('chat_id')).first()
        if guest:
            guest.active = False
            guest.save()
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    KOEF = settings.YANDEX_KOEF

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
            amount = settings.WITH_CODE_COST * guest.count
        else:
            amount = settings.WITHOUT_CODE_COST * guest.count
        if amount > 300:
            amount = round(amount/self.KOEF)
        attrs['amount'] = amount
        return attrs

    def get_link(self, obj):
        return payment_facade.get_terminal(obj.amount, obj.id)


class PromoterSerializer(serializers.ModelSerializer):

    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Promoter
        fields = ('id', 'name', 'guests_count', 'is_active', 'chat_id', 'total_payment')
        extra_kwargs = {
            'guests_count': {'read_only': True},
            'name': {'read_only': True},
            'total_payment': {'read_only': True}
        }

    def update(self, instance, validated_data):
        if instance.is_active:
            raise Http404
        return super().update(instance, validated_data)


class PromoCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromoCode
        fields = ('id', 'name', 'promoter')

    @staticmethod
    def validate_promoter(value):
        if not value.is_active:
            raise PromoterInactive
        return value

    @staticmethod
    def validate_name(value):
        return value.lower()
