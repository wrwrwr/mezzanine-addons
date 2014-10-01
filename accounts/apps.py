from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Resolves a label clash with the ``mezzanine.accounts`` module.
    """
    name = 'accounts'
    label = 'accounts_addons'
