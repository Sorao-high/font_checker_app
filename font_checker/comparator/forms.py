from django import forms
from .models import FontFeature

class ComparisonForm(forms.Form):
    # DBから選択肢を動的に生成
    font_choices = list(FontFeature.objects.values_list('font_name', 'font_name').distinct())
    char_choices = list(FontFeature.objects.values_list('character', 'character').distinct().order_by('character'))

    font_name = forms.ChoiceField(label='お手本フォント', choices=font_choices, widget=forms.Select(attrs={'class': 'form-select'}))
    character = forms.ChoiceField(label='お手本文字', choices=char_choices, widget=forms.Select(attrs={'class': 'form-select'}))
    image = forms.ImageField(label='手書き文字の画像', widget=forms.FileInput(attrs={'class': 'form-control'}))