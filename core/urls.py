from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Mostra seu HTML
    path('qr/', views.ler_qr_code, name='ler_qr_code'),
    path('gabarito/', views.ler_gabarito, name='ler_gabarito'),
]

