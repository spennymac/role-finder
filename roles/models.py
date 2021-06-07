from django.db import models


# Create your models here.
class Entity(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    last_modified_dt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CloudProvider(Entity):
    name = models.CharField(max_length=127)
    code = models.CharField(max_length=127)

    def __str__(self):
        return self.name


class Permission(Entity):
    name = models.CharField(max_length=127, unique=True)

    def __str__(self):
        return self.name


class Role(Entity):
    name = models.CharField(max_length=127)
    title = models.CharField(max_length=127)
    cloud_provider = models.ForeignKey(CloudProvider, related_name='roles', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RolePermission(Entity):
    role = models.ForeignKey(Role, related_name='role_permissions', on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, related_name='role_permissions', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['role', 'permission'], name='role_permission_idx')
        ]
