from rest_framework.routers import DefaultRouter

from clients.api import views

router = DefaultRouter()
router.register('', views.ClientsViewSet, base_name='clients')

urlpatterns = router.urls
