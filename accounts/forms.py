from django import forms
from django.contrib.auth.models import User
from .models import Document  # Імпортуємо твою модель

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердіть пароль'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Імʼя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Паролі не збігаються!")
        return confirm_password

# НОВА ФОРМА ДЛЯ ЗАВАНТАЖЕННЯ ДОКУМЕНТІВ
class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document_type', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Наприклад: Договір оренди №123'
            }),
            'document_type': forms.Select(attrs={
                'class': 'form-select'  # Стиль Bootstrap для списку
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'title': 'Назва документа',
            'document_type': 'Оберіть тип документа',
            'file': 'Файл',
        }