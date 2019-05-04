from django.conf.urls import url, include
from rest_framework import serializers, viewsets, routers

from . import views
from .models import Post


class PostSerializer(serializers.ModelSerializer):
#    author = serializers.CharField
#    title = serializers.CharField
#    text = serializers.CharField
#    created_date = serializers.DateTimeField
#    published_date = serializers.DateTimeField
    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'created_date','published_date')

class DataViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

router = routers.DefaultRouter()
router.register(r'posts',DataViewSet)
urlpatterns = [
    url(r'^post_list/$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^', include(router.urls)),


]
