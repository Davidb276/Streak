from django.shortcuts import render

from django.shortcuts import render

def user_list_view(request):
    users = [
        {"name": "María López", "role": "Recruiter", "email": "maria@example.com"},
        {"name": "Carlos Pérez", "role": "Developer", "email": "carlos@example.com"},
        {"name": "Ana Torres", "role": "Data Analyst", "email": "ana@example.com"},
    ]
    return render(request, "users/user_list.html", {"users": users})


def profile_view(request):
    user_data = {
        "name": "David Bermúdez Velásquez",
        "email": "david@example.com",
        "role": "Backend Developer",
        "skills": ["Python", "Django", "SQL", "Docker"],
        "bio": "Apasionado por crear soluciones escalables y eficientes. Siempre aprendiendo algo nuevo.",
    }
    return render(request, "users/profile.html", {"user": user_data})
