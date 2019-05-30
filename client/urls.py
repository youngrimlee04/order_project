from django.conf.urls import url, include
# view 안에 index를 import
from .views import (
    index,signup,login,
)

urlpatterns = [
    url(r'^$',index, name="index"),
    url(r'^signup/$', signup,name="signup"),
    url(r'^login/$', login,name="login"),
]
