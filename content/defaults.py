from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting


register_setting(
    name='PARTNER_RELATION_CHOICES',
    label=_("Partner relationship types"),
    description=_("Different kinds of partners you may have."),
    editable=True,
    default=(
        ('main', _("Title or general sponsor")),
        ('official', _("Official sponsor")),
        ('technical', _("Technical sponsor")),
        ('participating', _("Participating sponsor")),
        ('informational', _("Media coverage")),
    ),
)
