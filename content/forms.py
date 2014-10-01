from django import forms
from django.utils.safestring import mark_safe

from mezzanine.core.templatetags.mezzanine_tags import thumbnail


class ImageWidgetBase(object):
    """
    Render a visible thumbnail for image fields.

    Extended `ImageWidget` from cartridge.forms to be used with Mezzanine.
    """
    def render(self, name, value, attrs):
        rendered = super(ImageWidgetBase, self).render(name, value, attrs)
        if value:
            orig = '%s%s' % (settings.MEDIA_URL, value)
            thumb = '%s%s' % (settings.MEDIA_URL, thumbnail(value, 48, 48))
            rendered = ('<a href="%s"> target="_blank"'
                        '<img style="margin-right: 6px;" src="%s">'
                        '</a><span class="clearable-image">%s</span>' %
                        (orig, thumb, rendered))
        return mark_safe(rendered)


class ImageWidget(ImageWidgetBase, forms.FileInput):
    pass


class ClearableImageWidget(ImageWidgetBase, forms.ClearableFileInput):
    pass
