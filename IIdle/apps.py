from django.apps import AppConfig


class IidleConfig(AppConfig):
    name = 'IIdle'

    def ready(self):
        import IIdle.signals  # noqa
