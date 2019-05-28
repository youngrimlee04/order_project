from django.conf.urls import url, include
# view 안에 index를 import
from .views import (
    index,
    edit_info,
    signup, login, logout, #auth
    menu
)

urlpatterns = [
    url(r'^$',index, name="index"),
    url(r'^signup/$', signup,name="signup"),
    url(r'^login/$', login,name="login"),
    url(r'^logout/$', logout,name="logout"),
    url(r'^edit/$', edit_info,name="edit"),
    url(r'^menu/$', menu,name="menu"),
]
