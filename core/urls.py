from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/",include('accounts.urls')),
    path("profile/", include('profiles.urls')),
    path("chat/",include('chat.urls')),
    path('auth/google/',include('drf_social_oauth2.urls',namespace='drf'))
]
