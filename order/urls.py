"""order URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.conf.urls import url, include
from django.contrib import admin

# 달러 표시가 urls.py-partner와 달리 없는 건
# 끝이 아니고 partner 뒤에 urls.py-partner다 이어진다
urlpatterns = [
    url(r'^partner/', include('partner.urls')),
    url(r'^admin/', admin.site.urls),
]
