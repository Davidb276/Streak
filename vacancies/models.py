# vacancies/models.py
from django.db import models
from users.models import User

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.CharField(max_length=255, help_text="Ejemplo: Python, Django, SQL")
    date_posted = models.DateTimeField(auto_now_add=True)
    applicants = models.ManyToManyField(User, related_name='vacancies_applied', blank=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"
