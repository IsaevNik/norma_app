"""norma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from core.views import CheckPromoCodeView, CreateGuestView, CreateOrderView, PaymentProcess, PaymentRedirectView, \
    IndexView, ActivatePromoterView, PromoterRetrieveView, CreatePromocodeView

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^web/check-promo-code/$', CheckPromoCodeView.as_view()),
    url(r'^web/guests/$', CreateGuestView.as_view()),
    url(r'^web/orders/$', CreateOrderView.as_view()),
    url(r'^payment/$', PaymentProcess.as_view()),
    url(r'^payment/fail/$', PaymentRedirectView.as_view()),
    url(r'^payment/success/$', PaymentRedirectView.as_view()),
    url(r'^web/promoters/(?P<activate_code>\w+)/$', ActivatePromoterView.as_view()),
    url(r'^web/promoters/(?P<pk>\d+)/statistic/$', PromoterRetrieveView.as_view()),
    url(r'^web/promo-codes/', CreatePromocodeView.as_view())
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)