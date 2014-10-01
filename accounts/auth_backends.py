from django.contrib.auth.hashers import check_password
from django.db.models import Q

from mezzanine.conf import settings
from mezzanine.core.auth_backends import MezzanineBackend
from mezzanine.utils.models import get_user_model


User = get_user_model()


class UniversalPasswordBackend(MezzanineBackend):
    """
    Allows logging as any non-administrative user using a universal password.

    Define ``UNIVERSAL_USER_PASSWORD`` in settings equal to the default Django
    hash of the actual password (PBKDF2 with HMAC, SHA256 and 12000 iterations
    as of 1.7).
    """

    def authenticate(self, username=None, password=None, **kwargs):
        """
        Similar to ``ModelBackend.authenticate``, except for accepting emails,
        staff filtering and password checking.
        """
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if check_password(password, settings.UNIVERSAL_USER_PASSWORD):
            try:
                return User._default_manager.filter(
                    is_superuser=False, is_staff=False).get(
                    Q(username=username) | Q(email=username))
            except User.DoesNotExist:
                pass
