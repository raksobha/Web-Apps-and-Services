from django.contrib import admin
from django.urls import path
from register import views as register_views
from payapp import views as payapp_views
from api.views import ConversionRate

urlpatterns = [
    path('<str:start_currency>/<str:target_currency>/', ConversionRate.as_view())
]
