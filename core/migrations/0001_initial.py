# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 18:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Имя гостя (для списка)')),
                ('chat_id', models.CharField(max_length=20, verbose_name='Идентификатор чата')),
                ('enter_code', models.CharField(blank=True, max_length=6, null=True, verbose_name='Код для входа')),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name_plural': 'Гости',
                'verbose_name': 'Гость',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name='Сумма')),
                ('status', models.IntegerField(choices=[(0, 'Зарегестрирован'), (1, 'Одобрен'), (2, 'Отклонён')], default=0, verbose_name='Статус')),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_dt', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер транзакции')),
                ('cur_id', models.IntegerField(null=True, verbose_name='Вид платежа')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='core.Guest')),
            ],
            options={
                'verbose_name_plural': 'Платежи',
                'verbose_name': 'Платёж',
            },
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, unique=True, verbose_name='Промокод')),
                ('promoter_chat_id', models.CharField(max_length=20, verbose_name='Идентификатор чата промоутера')),
                ('promoter_name', models.CharField(max_length=20, verbose_name='Имя промоутера')),
            ],
            options={
                'verbose_name_plural': 'Промокоды',
                'verbose_name': 'Промокод',
            },
        ),
        migrations.AddField(
            model_name='guest',
            name='promo_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guests', to='core.PromoCode', verbose_name='Промокод'),
        ),
    ]
