from django.shortcuts import render

def vacancies_view(request):
    jobs = [
        {"title": "Desarrollador Backend", "company": "TechNova", "location": "Remoto", "description": "Construcción de APIs y optimización de servicios."},
        {"title": "Analista de Datos", "company": "DataCorp", "location": "Bogotá, Colombia", "description": "Análisis de grandes volúmenes de datos y visualización de resultados."},
        {"title": "Diseñador UX/UI", "company": "Creativa Studio", "location": "Medellín, Colombia", "description": "Diseño de interfaces modernas centradas en el usuario."},
    ]
    return render(request, "vacancies.html", {"jobs": jobs})
