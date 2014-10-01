from copy import deepcopy

from django.contrib import admin
from django.db.models import ImageField
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.admin import TranslationAdmin
from mezzanine.pages.admin import PageAdmin

from .models import Banner, Partner, ImagePage, Section
from .forms import ImageWidget, ClearableImageWidget


dimensions_fieldset = \
    (_("Image parameters"), {
        'fields': ['image_scaling', 'image_width', 'image_height',
                   'image_quality'],
        'classes': ("collapse-closed",)
    })


class BannerAdmin(TranslationAdmin):
    list_display = ('key', 'image', 'link')
    list_editable = ('image', 'link')
    fieldsets = (
        (None, {'fields': ('key', 'image', 'link'),}),
        dimensions_fieldset
    )
    ordering = ('key',)
    formfield_overrides = {ImageField: {'widget': ImageWidget}}


class PartnerAdmin(TranslationAdmin):
    list_display = ('relation', 'name', 'logo', 'website')
    list_editable = ('relation', 'name', 'logo', 'website')
    fieldsets = (
        (None, {'fields': ('relation', 'name', 'description', 'logo',
                           'website'),}),
        dimensions_fieldset
    )
    ordering = ('relation', 'name')
    formfield_overrides = {ImageField: {'widget': ImageWidget}}


imagepage_fieldsets = list(deepcopy(PageAdmin.fieldsets))
imagepage_fieldsets[0][1]['fields'].insert(1, 'image')
imagepage_fieldsets[0][1]['fields'].insert(2, 'icon')
imagepage_fieldsets[0][1]['fields'].insert(3, 'content')
imagepage_fieldsets.insert(-1, dimensions_fieldset)


class ImagePageAdmin(PageAdmin):
    fieldsets = imagepage_fieldsets
    formfield_overrides = {ImageField: {'widget': ClearableImageWidget}}


section_fieldsets = deepcopy(imagepage_fieldsets)
section_fieldsets[0][1]['fields'].remove('icon')
section_fieldsets[0][1]['fields'].insert(1, 'display_categories')
section_fieldsets[0][1]['fields'].insert(3, 'color')


class SectionAdmin(ImagePageAdmin):
    fieldsets = section_fieldsets


admin.site.register(Banner, BannerAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(ImagePage, ImagePageAdmin)
admin.site.register(Section, SectionAdmin)
