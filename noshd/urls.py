"""noshd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from noshdapp import views
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from noshdapp.views import feed_view, following_view, followers_view


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'post', views.RestaurantPostViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'following', views.UserFollowingViewSet)


urlpatterns = [
    path('noshd/', include('noshdapp.urls')),
    path('admin/', admin.site.urls),
    path('feed/', feed_view),
    path(r'api-token-auth/', obtain_jwt_token),
    path(r'api-token-refresh/', refresh_jwt_token),
    url(r'^user/(?P<username>.+)/following', following_view),
    url(r'^user/(?P<username>.+)/followers', followers_view),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),

]
