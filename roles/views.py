from functools import reduce

from rest_framework import viewsets, filters

from roles.cache import get_trie, CloudProviders
from roles.models import Role, Permission, CloudProvider
from roles.serializers import RoleSerializer, PermissionSerializer


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'title']

    def get_queryset(self):

        cloud_provider: int = self.request.query_params.get('cloud_provider', None)
        permission: str = self.request.query_params.get('permission', None)

        if permission:
            permissions_trie = get_trie(cloud_provider=CloudProviders.GCP)
            try:
                all_roles = []
                permissions = permissions_trie.keys(permission)
                for p in permissions:
                    qs = permissions_trie.values(p)
                    all_roles.append(qs)
                res = reduce(lambda x, y: x | y, all_roles[0])
                self.queryset = res.distinct()
            except KeyError:
                return Role.objects.none()

        if cloud_provider:
            self.queryset = self.queryset.filter(cloud_provider=cloud_provider)

        return self.queryset


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']


class CloudProviderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CloudProvider.objects.all()
    serializer_class = PermissionSerializer
