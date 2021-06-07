from django.apps import AppConfig


class RolesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'roles'

    def ready(self):
        from roles.cache import reload_all
        reload_all()
