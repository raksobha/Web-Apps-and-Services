from django.contrib import admin
from django.urls import path, include
from register import views as register_views
from payapp import views as payapp_views
from api.views import ConversionRate
urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", payapp_views.home, name="home"),
    path("transactions/", payapp_views.transactions, name="transactions"),
    path("notifications/reject/<int:notif_id>/", payapp_views.reject_payment, name="reject_payment"),
    path("notifications/seen/<int:notif_id>/", payapp_views.seen_notification, name="seen_notification"),
    path("payment/makepayment/<int:notif_id>/", payapp_views.make_payment, name="make_payment"),
    path("payment/requestpayment", payapp_views.request_payment, name="request_payment"),
    path("notifications/", payapp_views.notifications, name="notifications"),
    path("signup/", register_views.signup_user, name="signup"),
    path("login/", register_views.login_user, name="login"),
    path("logout/", register_views.logout_user, name="logout"),
    path('api-auth/', include('rest_framework.urls')),
    #path('convert/<str:startCurrency>/<str:targetCurrency>/', ConversionRate.as_view(), name="conversion_rate"),
    path('conversion/', include('api.urls')),

]
