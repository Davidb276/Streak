from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, SignUpForm

# Lista de usuarios (solo para demo)
def user_list_view(request):
    users = [
        {"name": "María López", "role": "Recruiter", "email": "maria@example.com"},
        {"name": "Carlos Pérez", "role": "Developer", "email": "carlos@example.com"},
        {"name": "Ana Torres", "role": "Data Analyst", "email": "ana@example.com"},
    ]
    return render(request, "users/user_list.html", {"users": users})

# Perfil del usuario autenticado
@login_required
def profile_view(request):
    user = request.user
    user_data = {
        "bio": getattr(user, "bio", ""),
        "skills": getattr(user, "skills", ""),
        "level": getattr(user, "level", 1),
        "points": getattr(user, "points", 0),
        "profile_picture": getattr(user, "profile_picture", None),
    }
    if user_data["skills"]:
        user_data["skills_list"] = [s.strip() for s in user_data["skills"].split(",")]
    else:
        user_data["skills_list"] = []
    return render(request, "users/profile.html", {"user_data": user_data})

# Vista para editar perfil (solo bio y skills)
@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("users:profile")
    else:
        form = ProfileForm(instance=user)
    return render(request, "users/edit_profile.html", {"form": form})

# Vista de registro (signup) usando el formulario personalizado
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente
            return redirect("users:profile")  # Redirige a su perfil
        else:
            messages.error(request, "Por favor corrige los errores del formulario")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})
