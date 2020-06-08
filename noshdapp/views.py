from django.http import HttpResponse
from .models import RestaurantPost, User, UserFollowing
from rest_framework import viewsets
from noshdapp.serializers import RestaurantPostSerializer, RegistrationSerializer, UserSerializer, FollowingSerializer, FollowersSerializer
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .renderers import UserJSONRenderer
from rest_framework.decorators import api_view
from django.views.generic import ListView



from django.contrib.auth.models import Group


class RestaurantPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = RestaurantPost.objects.all()
    serializer_class = RestaurantPostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
def feed_view(request, *args, **kwargs):
    user = request.user
    qs = RestaurantPost.objects.feed(user)
    serializer = RestaurantPostSerializer(qs, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def following_view(request, username, *args, **kwargs):
    obj = User.objects.get(username__iexact=username)
    qs = obj.following.all()
    serializer = FollowingSerializer(qs, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def followers_view(request, username, *args, **kwargs):
    obj = User.objects.get(username__iexact=username)
    qs = obj.followers.all()
    serializer = FollowersSerializer(qs, many=True)
    return Response(serializer.data, status=200)


# class FeedView(viewsets.ModelViewSet):
#
#     def feed_view(self, *args, **kwargs):
#         user = self.request.user
#         qs = RestaurantPost.objects.feed(user)
#         serializer = RestaurantPostSerializer(qs, many=True)
#         return Response(serializer.data, status=200)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserFollowingViewSet(viewsets.ModelViewSet):
    queryset = UserFollowing.objects.all()
    serializer_class = FollowingSerializer

