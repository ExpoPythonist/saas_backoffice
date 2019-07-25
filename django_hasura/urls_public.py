from django.contrib import admin
from django.urls import path, include
from django_cloud_tasks import urls as dct_urls
from rest_framework_swagger.views import get_swagger_view

from clients.views import HomePageView

schema_view = get_swagger_view(title='Django SAAS API')

api_patterns = [
    path('clients/', include('clients.api.urls')),
    path('users/', include('users.api.urls')),
]

urlpatterns = [
    path('', HomePageView.as_view()),
    path('docs/', schema_view),
    path('admin/', admin.site.urls),
    path('hasura/', include('hasura.urls')),
    path('api/v1/', include(api_patterns)),
]

urlpatterns += [path('_tasks/', include(dct_urls))]
