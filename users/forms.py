from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'skills']  # Solo los campos editables
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Separadas por comas'}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    skills = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Separadas por comas'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'skills', 'password1', 'password2']
