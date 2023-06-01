from django.urls import path
from onlineshop_app.api.views import (OrderView,)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('order/', OrderView.as_view(), name='order'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
