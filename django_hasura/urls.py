from django.contrib import admin
from django.urls import path, include

from clients import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view()),
    path('api/v1/users/', include('users.api.urls')),
]
