from django.http import HttpResponse
from .models import Post
from rest_framework import viewsets
from noshdapp.serializers import PostSerializer, UserSerializer, GroupSerializer
from django.shortcuts import render
from django.contrib.auth.models import User, Group



class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


def index(request):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

