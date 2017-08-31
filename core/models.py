from django.db import models

from core.utils import norma_bot, generate_code

__all__ = ['PromoCode', 'Guest', 'Order']


class PromoCode(models.Model):
    name = models.CharField(max_length=20, unique=True, db_index=True, verbose_name='Промокод')
    promoter_chat_id = models.CharField(max_length=20, verbose_name='Идентификатор чата промоутера')
    promoter_name = models.CharField(max_length=20, verbose_name='Имя промоутера')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


class Guest(models.Model):
    name = models.CharField(max_length=64, verbose_name='Имя гостя (для списка)')
    chat_id = models.CharField(max_length=20, verbose_name='Идентификатор чата')
    promo_code = models.ForeignKey(PromoCode, blank=True, null=True,
                                   related_name='guests', verbose_name='Промокод')
    enter_code = models.CharField(max_length=6, null=True, blank=True, verbose_name='Код для входа')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    count = models.IntegerField(default=1, verbose_name='Количество билетов')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'

    def send_success(self):
        norma_bot.send_success(self)

    def send_fail(self):
        norma_bot.send_fail(self)

    def generate_enter_code(self):
        self.enter_code = generate_code(6)
        self.save()


class Order(models.Model):
    REGISTERED = 0
    DEPOSITED = 1
    DECLINED = 2
    STATUSES = ((REGISTERED, 'Зарегестрирован'),
                (DEPOSITED, 'Одобрен'),
                (DECLINED, 'Отклонён'))
    amount = models.IntegerField(default=0, verbose_name='Сумма')
    status = models.IntegerField(choices=STATUSES, default=REGISTERED, verbose_name='Статус')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_dt = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    transaction_id = models.CharField(max_length=100, null=True, blank=True,
                                      verbose_name='Номер транзакции')
    cur_id = models.IntegerField(null=True, verbose_name='Вид платежа')
    guest = models.ForeignKey(Guest, related_name='orders')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'

    @staticmethod
    def accept_order(data):
        order_id = data.get('MERCHANT_ORDER_ID')
        cur_id = data.get('CUR_ID')
        intid = data.get('intid')
        order = Order.objects.get(id=order_id)
        order.cur_id = int(cur_id)
        order.transaction_id = int(intid)
        order.status = Order.DEPOSITED
        order.save()
        return order
