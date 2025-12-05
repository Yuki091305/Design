from django import forms
from .models import DesignRequest

class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        # Пользователь заполняет только название, описание и выбирает категорию
        fields = ['title', 'description', 'category']