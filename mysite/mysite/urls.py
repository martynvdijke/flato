"""mysite URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers
from django.apps import apps

'''
Serializes the users info 
'''
class UserSerializer(serializers.HyperlinkedModelSerializer):
    # profile = ProfileSerializer()
    # room_status = serializers.CharField(source='profile.room_status')
    # wheater_city = serializers.CharField(source='profile.wheater_city')

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name','last_name','last_login','date_joined')





'''
ViewSets define the view behavior.
'''
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
2
'''
Add the url to django
'''
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^', include('flato.urls')),
    url(r'^', include('blog.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^rest/', include('rest_framework.urls', namespace='rest_framework')),

]

urlpatterns += staticfiles_urlpatterns()

