from django.shortcuts import render

def vacancy_list(request):
    return render(request, 'vacancies/vacancy_list.html')
