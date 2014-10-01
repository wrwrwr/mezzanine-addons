from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.pages.models import Page, RichText
from mezzanine.utils.models import AdminThumbMixin, upload_to

from utils.fields import URLField


class ImageParameters(models.Model):
    """
    Base class for models with images that should be "twinkable"
    through admin.
    """ 
    image_scaling = models.BooleanField(_("Automatic scaling"), default=True,
        help_text=_("Should the image be scaled and/or clipped to fit the "
                    "specified output dimensions or place reserved in "
                    "templates? Note that without scaling, if the uploaded "
                    "image is larger than expected, layout may break."))
    image_quality = models.IntegerField(_("Quality"), default=95,
        help_text=_("Compression level of the output image. 100 means best "
                    "quality, but largest file size, 0 worst quality, and "
                    "smallest file size. Typical values are within 80-100."))
    image_width = models.IntegerField(_("Image width"), default=0,
        help_text=_("Output width of the image. Enter zero to calculate from "
                    "height. Zero both dimensions to fit to template."))
    image_height = models.IntegerField(_("Image height"), default=0,
        help_text=_("Output height of the image. Enter zero to calculate from "
                    "width. Zero both dimensions to fit to template."))

    class Meta:
        abstract = True


class Banner(ImageParameters, AdminThumbMixin):
    """
    Banners that can be changed through administration.
    
    Add a ``{% banner "location-key" width height %}`` to template and
    create an object with the same ``location-key`` through admin.
    """
    key = models.CharField(_("Template key"), max_length=50,
        help_text=_("String used in templates to identify this banner. "
                    "New identifiers have to be inserted into templates "
                    "before they'll appear anywhere on the site."))
    image = models.ImageField(_("Image"),
        upload_to=upload_to('content.Banner.image', 'banners'),
        help_text=_("Image or animation. Most common image formats may be "
                    "uploaded."))
    link = URLField(_("Link"), blank=True,
        help_text=_("Page to go to if the user clicks on the image. You may "
                    "enter a path for the current site (e.g. \"/news\") or an "
                    "absolute URL. Leave empty for an unclickable banner."))

    class Meta:
        verbose_name = _("banner")
        verbose_name_plural = _("banners")

    def __unicode__(self):
        return self.key


class Partner(ImageParameters, AdminThumbMixin):
    """
    For storing and displaying partner logos with various categories of
    partners.
    """
    RELATION_CHOICES = settings.PARTNER_RELATION_CHOICES
    relation = models.CharField(_("Relation"),
        max_length=50, choices=RELATION_CHOICES,
        default=RELATION_CHOICES[0][0])
    name = models.CharField(_("Partner name"),
        max_length=255,
        help_text=_("Alternate text for images."))
    description = models.CharField(_("Short description"),
        max_length=255,
        help_text=_("Description displayed below image on partners list."))
    logo = models.ImageField(_("Logo"),
        upload_to=upload_to('content.Partner.image', 'partners'))
    website = URLField(_("Partner's web page"), blank=True,
        help_text=_("If the user clicks partner's logo or link, this website "
                    "will be opened in a new browser tab."))

    class Meta:
        ordering = ('relation',)
        verbose_name = _("partner")
        verbose_name_plural = _("partners")


class ImagePage(Page, RichText, ImageParameters, AdminThumbMixin):
    """
    Rich text page with a privileged image.
    """
    image = models.ImageField(_("Main image"), blank=True,
        upload_to=upload_to('content.ImagePage.image', 'pages'),
        help_text=_("The image main page's image, may be configured using "
                    "image parameters."))
    icon = models.ImageField(_("Icon"), blank=True,
        upload_to=upload_to('content.ImagePage.icon', 'pages'),
        help_text=_("Small icon for the page, if it's not provided the main "
                    "image is used."))

    class Meta:
        verbose_name = _("image page")
        verbose_name_plural = _("image pages")


class Section(ImagePage):
    """
    Super-category for Cartridge.

    Good if your top categories won't contain any products, but will need
    some more attributes than lower-level categories.
    """
    color = models.CharField(_("Section color"),
        max_length=20, default='#333333',
        help_text=_("Color of the text overlay."))
    display_categories = models.BooleanField(_("Display categories"),
        default=True,
        help_text=_("Section may be displayed as a list of assigned "
                    "categories or an image with text overlay."))

    class Meta:
        verbose_name = _("section")
        verbose_name_plural = _("sections and categories")  # TODO: Admin template?

# Customize upload directory and help text for the main `Section` image.
section_image_field = Section._meta.get_field('image')
section_image_field.upload_to=upload_to('catalog.Section.image', 'sections'),
section_image_field.help_text=_("The image shown on front page or when"
                                "section is set not to display categories.")
