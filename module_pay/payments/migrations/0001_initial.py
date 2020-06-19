# Generated by Django 3.0.7 on 2020-06-19 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='', max_length=1500, verbose_name='Название услуги')),
                ('amount', models.IntegerField(verbose_name='Стоимость')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_bank', models.CharField(max_length=100, verbose_name='Название банка')),
                ('order_id', models.IntegerField(verbose_name='Номер счета')),
                ('bank_response', models.BooleanField(blank=True, default=False, verbose_name='Ответ банка')),
                ('time_transaction', models.DateTimeField(verbose_name='Время транзакции')),
                ('detail_response', models.TextField(blank=True, default='', max_length=1500, verbose_name='Детальный ответ')),
                ('time_confirmed', models.DateTimeField(blank=True, verbose_name='Время подтверждения')),
                ('payment_confirmed', models.BooleanField(blank=True, default=False, verbose_name='Платеж подтверждён')),
                ('comments', models.TextField(blank=True, default='', max_length=1500, verbose_name='Комментарии')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус транзакции')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Удален')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='payments.Products')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
