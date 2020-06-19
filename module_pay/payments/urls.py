from django.urls import include, path
from . import views

urlpatterns = [
    path('payments/', views.payments_view, name='payments'),
    path('success/', views.payments_complete, name='success'),
    path('confirm/', views.pay_confirm, name='confirm'),
    path('result/', views.pay_result, name='result'),
    path('failure/', views.pay_failure, name='failure'),
]