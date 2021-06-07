from typing import Set, Tuple

from django.core.management.base import BaseCommand
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

from roles.models import CloudProvider, Role, Permission, RolePermission


class Command(BaseCommand):

    def handle(self, *args, **options):

        cloud_provider, _ = CloudProvider.objects.get_or_create(code="GCP")
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build('iam', 'v1', credentials=credentials)
        request = service.roles().list()

        while True:
            response = request.execute()

            for role in response.get('roles', []):
                request = service.roles().get(name=role['name'])
                role_details = request.execute()
                role_instance, _ = Role.objects.get_or_create(
                    cloud_provider=cloud_provider,
                    name=role_details['name'],
                    title=role_details['title']
                )
                # Find current loaded permissions
                gcp_permissions = set(role_details['includedPermissions'])

                current_permissions_by_name = set(
                    role_instance.role_permissions.values_list('permission__name', flat=True))
                need_to_delete = current_permissions_by_name - gcp_permissions

                # Reconcile
                RolePermission.objects.filter(permission__name__in=need_to_delete).delete()

                bulk = []
                for p in role_details['includedPermissions']:
                    permission_instance, _ = Permission.objects.get_or_create(name=p)
                    bulk.append(RolePermission(
                        role=role_instance,
                        permission=permission_instance
                    ))

                RolePermission.objects.bulk_create(bulk, ignore_conflicts=True)

            request = service.roles().list_next(previous_request=request, previous_response=response)
            if request is None:
                break

        self.stdout.write(self.style.SUCCESS('Successfully loaded all roles/permissions for google cloud!'))
