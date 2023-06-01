from django.urls import path
from onlineshop_app.api.views import (OrderView,)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('order/', OrderView.as_view(), name='order'),
]
