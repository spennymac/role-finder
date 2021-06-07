from rest_framework import serializers

from roles.models import Role, Permission, RolePermission, CloudProvider


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['title', 'name']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name']


class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ['role', 'permission']

class CloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudProvider
        fields = ['pk', 'name', 'code']
