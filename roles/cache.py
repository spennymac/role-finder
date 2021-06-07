from enum import Enum

import pygtrie

from roles.models import Permission, Role, CloudProvider


class CloudProviders(Enum):
    GCP = "GCP"
    AWS = "AWS"


_PERMISSION_TRIES = {
    CloudProviders.GCP: pygtrie.StringTrie(separator='.'),
    CloudProviders.AWS: pygtrie.CharTrie(),
}


def reload_trie(identifier: CloudProviders):
    for p in Permission.objects.all():
        roles = Role.objects.filter(
            cloud_provider=CloudProvider.objects.filter(code=identifier.value).first(),
            role_permissions__permission=p
        )
        _PERMISSION_TRIES[identifier][p.name] = roles


def reload_all():
    reload_trie(CloudProviders.GCP)
    # reload_trie(CloudProviders.AWS)


def get_trie(cloud_provider: CloudProviders, reload=False):
    if reload:
        reload_trie(identifier=cloud_provider)
    return _PERMISSION_TRIES[cloud_provider]
