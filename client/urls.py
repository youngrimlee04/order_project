from django.conf.urls import url, include
# view 안에 index를 import
from .views import (
    index,
)

urlpatterns = [
    url(r'^$',index, name="index"),
]
