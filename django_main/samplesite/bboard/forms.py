from django.forms import ModelForm
from .models import Bb

from django import forms
from django.forms import inlineformset_factory
from .models import Bb, BbFeature, BbImage

class BbForm(ModelForm):
    class Meta:
     model = Bb
     fields = ('title', 'content', 'price', 'rubric')

FeatureFormSet = inlineformset_factory(
    Bb,            # Родительская модель
    BbFeature,     # Связанная модель
    fields=('name', 'value'), # Поля, которые будут в строке
    extra=1,       # Сколько пустых строк показать сразу (по умолчанию)
    can_delete=True # Позволяет пользователю помечать записи на удаление
)

ImageFormSet = inlineformset_factory(
    Bb,
    BbImage,
    fields=('image', 'description'),
    extra=1,
    can_delete=True
)