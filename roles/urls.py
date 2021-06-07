from django.urls import path, include, re_path
from rest_framework import routers

from roles import views

router = routers.DefaultRouter()
router.register(r'roles', views.RoleViewSet)
router.register(r'permissions', views.PermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
