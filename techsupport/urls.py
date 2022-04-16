"""techsupport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from base import views
from base.type_geters import UserTypes, RequestTypes, FileTypes
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.UsersView.as_view(), name='users'),
    path('tickets/', views.TicketsView.as_view(), name='tickets'),
    path('file/<str:fileName>/', views.FilePostView.as_view(), name='file_upload'),
    path('file/', views.FileGetView.as_view(), name='file_get'),
    path('usertypes/', UserTypes.as_view(), name='usertypes'),
    path('requesttypes/', RequestTypes.as_view(), name='requesttypes'),
    path('filetypes/', FileTypes.as_view(), name='filetypes'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
