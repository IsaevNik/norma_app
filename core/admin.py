from django.contrib import admin

from core.models import Guest, PromoCode, Order


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'enter_code', 'promo_code', 'chat_id']


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'promoter_name', 'promoter_chat_id']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'transaction_id', 'status', 'create_dt']
