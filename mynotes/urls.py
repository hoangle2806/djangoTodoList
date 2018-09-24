"""mynotes URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from note import endpoints
from note import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #rest framework apis
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('knox.urls')),
    url(r'^api/', include(endpoints)),

    #front end navigation
    url(r'^$',views.home, name= 'home'),
    url(r'^login/$',views.logInView, name= 'logInView'),
    url(r'^user/(?P<username>\w{0,50})/(?P<token>.*)/$',views.UserView, name= 'UserView'),
    url(r'^register/$', views.RegisterView, name= 'registerView'),
    url(r'^delete/(?P<username>\w{0,50})/(?P<note_id>\d+)/(?P<token>.*)/$', views.DeleteView, name="deleteView"),
    url(r'^update/(?P<username>\w{0,50})/(?P<note_id>\d+)/(?P<token>.*)/$', views.EditView, name="editView"),

]