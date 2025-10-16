from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Vacancy
from .forms import VacancyForm

# --- Decorador para staff o superusuario ---
def staff_or_superuser_required(view_func):
    return user_passes_test(lambda u: u.is_staff or u.is_superuser)(view_func)

# --- Lista de vacantes ---
@login_required(login_url='login')
def vacancy_list(request):
    vacancies = Vacancy.objects.all().order_by('-date_posted')
    return render(request, "vacancies/vacancy_list.html", {"vacancies": vacancies})

# --- Crear vacante (solo staff/superuser) ---
@login_required
@staff_or_superuser_required
def vacancy_create(request):
    if request.method == "POST":
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("vacancies:list")
    else:
        form = VacancyForm()
    return render(request, "vacancies/vacancy_form.html", {"form": form, "action": "Crear"})

# --- Editar vacante (solo staff/superuser) ---
@login_required
@staff_or_superuser_required
def vacancy_update(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if request.method == "POST":
        form = VacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            return redirect("vacancies:list")
    else:
        form = VacancyForm(instance=vacancy)
    return render(request, "vacancies/vacancy_form.html", {"form": form, "action": "Editar"})

# --- Borrar vacante (solo staff/superuser) ---
@login_required
@staff_or_superuser_required
def vacancy_delete(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if request.method == "POST":
        vacancy.delete()
        return redirect("vacancies:list")
    return render(request, "vacancies/vacancy_confirm_delete.html", {"vacancy": vacancy})

# --- Aplicar a vacante (usuarios normales) ---
@login_required
def vacancy_apply(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    user = request.user

    # Si el usuario ya aplicó, se elimina (toggle)
    if user in vacancy.applicants.all():
        vacancy.applicants.remove(user)
    else:
        vacancy.applicants.add(user)

    return redirect("vacancies:list")
