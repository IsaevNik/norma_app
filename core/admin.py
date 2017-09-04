from django.contrib import admin

from core.models import Guest, PromoCode, Order, Promoter


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'enter_code', 'promo_code', 'is_came']
    search_fields = ('name', 'enter_code')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Promoter)
class PromoterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'chat_id', 'cost_by_person', 'is_active', 'guests_count', 'total_payment']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'transaction_id', 'status', 'create_dt']
