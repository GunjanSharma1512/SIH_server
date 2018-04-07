"""SIH_server URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from Login.views import unhash
# from Login.views import constraint_match
from Login.views import constraint_match, registerit,listeners,agency,flamingo,localhost,fh1,fh2
from Login.views import constraint_match, registerit



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^unhash/', unhash),
    url(r'^constraint_match/', constraint_match),
    url(r'^register/', registerit),
    url(r'^check/',listeners),
    url(r'^agency/', agency),
    url(r'^register/', registerit),
    url(r'^flamingo/', flamingo,name='flamingo'),
    url(r'^localhost/', localhost,name='localhost'),
    url(r'^h1/', fh1,name='h1'),
    url(r'^h2/', fh2,name='h2'),


]

