from django import forms
from .models import Vacancy, Company

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['company', 'title', 'description', 'tags']
