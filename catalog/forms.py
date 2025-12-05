from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from .models import DesignRequest

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")
    full_name = forms.CharField(max_length=100, label="ФИО")
    consent = forms.BooleanField(label="Согласие на обработку персональных данных")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_full_name(self):
        name = self.cleaned_data['full_name']
        if not re.match(r'^[а-яА-ЯёЁ\s\-]+$', name):
            raise ValidationError("Только кириллица, пробелы и дефис")
        return name

    def clean_username(self):
        u = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z\-]+$', u):
            raise ValidationError("Только латиница и дефис")
        return u

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError("Пароли не совпадают")
        return cd['password2']

class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'attachment']

class AdminStatusForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['status', 'admin_comment', 'design_image']
        widgets = {'admin_comment': forms.Textarea(attrs={'rows': 3})}

    def clean(self):
        cd = super().clean()
        status = cd.get('status')
        comment = cd.get('admin_comment')
        image = cd.get('design_image')

        if status == 'in_progress' and not comment:
            raise forms.ValidationError("Нужен комментарий при статусе 'Принято в работу'")
        if status == 'completed' and not image:
            raise forms.ValidationError("Нужно приложить фото при статусе 'Выполнено'")
        if self.instance.status != 'new' and status != self.instance.status:
            raise forms.ValidationError("Менять статус можно только у 'Новой' заявки")
        return cd