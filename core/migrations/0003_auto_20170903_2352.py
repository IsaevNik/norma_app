# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 20:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_guest_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promoter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=20, verbose_name='Идентификатор чата промоутера')),
                ('name', models.CharField(max_length=20, verbose_name='Имя промоутера')),
                ('cost_by_person', models.IntegerField()),
                ('activate_code', models.CharField(max_length=10, verbose_name='Код активации')),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Промоутеры',
                'verbose_name': 'Промоутер',
            },
        ),
        migrations.RemoveField(
            model_name='promocode',
            name='promoter_chat_id',
        ),
        migrations.RemoveField(
            model_name='promocode',
            name='promoter_name',
        ),
        migrations.AddField(
            model_name='promocode',
            name='promoter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promo_codes', to='core.Promoter', verbose_name='Промоутер'),
        ),
    ]
