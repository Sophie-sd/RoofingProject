from django import forms

from core.content_services import DEFAULT_HOME_BLOCKS, TEXT_FIELD_KEYS
from core.models import ContentPage, HomeBlock
from core.page_content import CONTENT_PAGES

CONTENT_PAGE_TEXT_FIELDS = ('title', 'eyebrow', 'lead', 'body', 'header_image_url')


def _apply_field_defaults(form, defaults, field_names, instance=None):
    if form.is_bound:
        return
    for name in field_names:
        if name not in form.fields:
            continue
        current = ''
        if instance is not None:
            current = getattr(instance, name, '') or ''
        if not current:
            default_val = defaults.get(name, '')
            if default_val:
                form.initial[name] = default_val


class HomeBlockAdminForm(forms.ModelForm):
    class Meta:
        model = HomeBlock
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = self.instance
        if not instance or not instance.pk:
            return
        block_defaults = DEFAULT_HOME_BLOCKS.get(instance.key, {})
        _apply_field_defaults(self, block_defaults, TEXT_FIELD_KEYS, instance)

    def save(self, commit=True):
        instance = super().save(commit=False)
        block_defaults = DEFAULT_HOME_BLOCKS.get(instance.key, {})
        for field in TEXT_FIELD_KEYS:
            if not getattr(instance, field, ''):
                setattr(instance, field, block_defaults.get(field, ''))
        if commit:
            instance.save()
        return instance


class ContentPageAdminForm(forms.ModelForm):
    class Meta:
        model = ContentPage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = self.instance
        if not instance or not instance.slug:
            return
        page_defaults = CONTENT_PAGES.get(instance.slug, {})
        if not page_defaults:
            return
        _apply_field_defaults(self, page_defaults, CONTENT_PAGE_TEXT_FIELDS, instance)

    def save(self, commit=True):
        instance = super().save(commit=False)
        page_defaults = CONTENT_PAGES.get(instance.slug, {})
        for field in CONTENT_PAGE_TEXT_FIELDS:
            if not getattr(instance, field, ''):
                setattr(instance, field, page_defaults.get(field, ''))
        if commit:
            instance.save()
        return instance
