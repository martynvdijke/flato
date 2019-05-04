from .models import Post
from rest_framework import serializers, viewsets, routers
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import include, url



class PostSerializer(serializers.HyperlinkedModelSerializer):
#    author = serializers.CharField
#    title = serializers.CharField
#    text = serializers.CharField
#    created_date = serializers.DateTimeField
#    published_date = serializers.DateTimeField
    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'created_date','published_date')

class DataViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()[:1]
    serializer_class = PostSerializer

router = routers.DefaultRouter()
router.register(r'data',DataViewSet)
