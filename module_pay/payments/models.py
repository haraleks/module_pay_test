import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django import forms

class Orders(models.Model):
    """модель для сохранения информации о транзакциях"""
    users = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)  #Forengnkey reletionship with users model
    name_bank = models.CharField('Название банка', blank=False, null=False, max_length=100)  # выбирать из списка
    product = models.ForeignKey('Products', on_delete=models.DO_NOTHING)
    order_id = models.IntegerField('Номер счета', blank=False, null=False) #Генерируем число от 2000001

    # time_response = models.DateTimeField('Время ответа банка', blank=True, null=False)
    bank_response = models.BooleanField('Ответ банка', null=False, default=False, blank=True)
    time_transaction = models.DateTimeField('Время транзакции', blank=False, null=True)  #скорее всего не нужно так как есть поле создание будет добавлятсья или при создании автоматически или запроса
    detail_response = models.TextField('Детальный ответ', blank=True, max_length=1500, default='') #код авторизации должен быть 00, если что то другое то транзакция неудачная

    time_confirmed = models.DateTimeField('Время подтверждения', blank=True, null=True)
    payment_confirmed = models.BooleanField('Платеж подтверждён', null=False, default=False, blank=True)
    comments = models.TextField('Комментарии', blank=True, max_length=1500, default='')

    is_active = models.BooleanField('Статус транзакции', null=False, default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    deleted_at = models.DateTimeField('Удален', null=True, default=None, blank=True)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.deleted_at = datetime.now()
        self.save()

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"


class Products(models.Model):
    name = models.CharField('Название услуги', blank=False, max_length=150, default='')
    amount = models.IntegerField('Стоимость', blank=False, null=False)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.deleted_at = datetime.now()
        self.save()

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class PayForm(forms.Form):
    product = forms.ModelMultipleChoiceField(queryset=Products.objects.all())