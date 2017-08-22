from django.conf.urls import url, include
from .views import OLRDialerViewset, index


urlpatterns = [
    url(r'insert', OLRDialerViewset.as_view()),
]