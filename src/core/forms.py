from django import forms

from .data import (
    AREA_CHOICES,
    FLOORS_CHOICES,
    ROOF_MATERIALS,
    WORK_TYPE_CHOICES,
)

_FIELD_CLASS = 'home-cta-form__input'
_SELECT_CLASS = 'home-cta-form__input home-cta-form__select'


class EstimateForm(forms.Form):
    email = forms.EmailField(
        label='Електронна пошта',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'ВАША EMAIL-АДРЕСА',
            'autocomplete': 'email',
        }),
    )


class EstimateRequestForm(forms.Form):
    settlement = forms.CharField(
        label='Населений пункт',
        max_length=120,
        widget=forms.TextInput(attrs={
            'class': _FIELD_CLASS,
            'placeholder': 'Біла Церква, Гатне...',
            'autocomplete': 'address-level2',
        }),
    )
    work_type = forms.ChoiceField(
        label='Тип робіт',
        choices=WORK_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': _SELECT_CLASS}),
    )
    area = forms.ChoiceField(
        label='Площа даху',
        choices=AREA_CHOICES,
        widget=forms.Select(attrs={'class': _SELECT_CLASS}),
    )
    floors = forms.ChoiceField(
        label='Поверхів будівлі',
        choices=FLOORS_CHOICES,
        widget=forms.Select(attrs={'class': _SELECT_CLASS}),
    )
    material = forms.ChoiceField(
        label='Покрівельний матеріал',
        choices=ROOF_MATERIALS,
        widget=forms.Select(attrs={'class': _SELECT_CLASS}),
    )
    phone = forms.CharField(
        label='Номер телефону',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': _FIELD_CLASS,
            'placeholder': '+380 00 000 00 00',
            'autocomplete': 'tel',
            'inputmode': 'tel',
        }),
    )


class CallbackForm(forms.Form):
    name = forms.CharField(
        label="Ваше ім'я",
        max_length=120,
        widget=forms.TextInput(attrs={
            'class': _FIELD_CLASS,
            'placeholder': "Ім'я та прізвище",
            'autocomplete': 'name',
        }),
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': _FIELD_CLASS,
            'placeholder': '+380 (__) ___ __ __',
            'autocomplete': 'tel',
            'inputmode': 'tel',
        }),
    )
    message = forms.CharField(
        label='Повідомлення',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'home-cta-form__input home-cta-form__textarea',
            'placeholder': 'Опишіть ваш запит...',
            'rows': 4,
        }),
    )
