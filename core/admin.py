from django.contrib import admin
from django.conf import settings

from core.models import Guest, PromoCode, Order, Promoter


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'chat_id', 'enter_code', 'promo_code', 'is_came', 'count_came', 'count']
    search_fields = ('name', 'enter_code')
    list_editable = ('is_came', 'count_came')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if settings.ONLY_ACTIVE:
            return qs.filter(active=True, enter_code__isnull=False)
        return qs


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Promoter)
class PromoterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'chat_id', 'cost_by_person', 'is_active', 'guests_count', 'total_payment']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'transaction_id', 'status', 'create_dt']
