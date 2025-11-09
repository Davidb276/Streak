from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from ai_module.openai_client import generate_text
from .models import Challenge, UserChallenge
import random
import re

@login_required
def retos_personalizados(request):
    user = request.user
    user_data = {
        "bio": user.bio,
        "skills": user.skills,
        "level": user.level,
        "points": user.points,
        "skills_list": [s.strip() for s in user.skills.split(",")] if user.skills else []
    }

    # Recuperar retos generados de la sesión si existen
    retos = request.session.get("retos_generados", [])

    # Generar nuevos retos si se solicita
    if request.GET.get("generate") == "1":
        semilla = random.randint(1000, 9999)

        prompt = f"""
Usuario con las siguientes características:
- Skills: {user_data['skills']}
- Nivel actual: {user_data['level']}
- Puntos acumulados: {user_data['points']}
- Bio: {user_data['bio']}

Genera tres retos completamente diferentes entre sí, personalizados para el usuario anterior.
Cada reto debe tener el formato:
Reto X: [título corto en una línea]
[descripción breve, 2-3 líneas como máximo]

❌ No incluyas introducción, títulos como “Vacante” o “Proyecto”, ni explicaciones extra.
Solo escribe los tres retos.
Semilla aleatoria: {semilla}
"""

        retos_generados = generate_text(prompt, mode="descripcion")

        # Limpieza de texto
        retos_generados = re.sub(r'(?i)(vacante|proyecto|rol|introducción|objetivo):.*$', '', retos_generados, flags=re.MULTILINE)
        bloques = re.split(r'(?=Reto\s*\d*[:\-]|Desaf[ií]o\s*\d*[:\-])', retos_generados, flags=re.IGNORECASE)
        retos = [b.strip() for b in bloques if b.strip().lower().startswith(("reto", "desaf"))][:3]

        # Extraer título y descripción
        retos_limpios = []
        for bloque in retos:
            lineas = bloque.split("\n", 1)
            titulo = lineas[0].strip()
            descripcion = lineas[1].strip() if len(lineas) > 1 else "Descripción no disponible."
            retos_limpios.append({"titulo": titulo, "descripcion": descripcion})
        retos = retos_limpios

        # Guardar en sesión
        request.session["retos_generados"] = retos

    # Retos completados por el usuario
    retos_completados = UserChallenge.objects.filter(user=user, completed=True).select_related('challenge')

    # Mapear los datos para la plantilla
    retos_completados_data = []
    for uc in retos_completados:
        retos_completados_data.append({
            "titulo": uc.challenge.title,
            "descripcion": uc.challenge.description,
            "score": uc.score,
            "completed_at": uc.completed_at
        })

    return render(request, "challenges/challenge_list.html", {
        "user_data": user_data,
        "retos": retos,
        "retos_completados": retos_completados_data
    })


@login_required
def completar_reto(request, reto_index):
    user = request.user
    try:
        # Recuperar reto de la sesión
        retos = request.session.get("retos_generados", [])
        if not retos or int(reto_index) >= len(retos):
            return JsonResponse({"success": False, "message": "Reto no encontrado"})

        reto_data = retos[int(reto_index)]
        titulo = reto_data["titulo"]
        descripcion = reto_data["descripcion"]

        # Crear Challenge si no existe
        challenge, created = Challenge.objects.get_or_create(title=titulo, defaults={"description": descripcion, "points": 10})

        # Registrar UserChallenge
        user_challenge, created_uc = UserChallenge.objects.get_or_create(user=user, challenge=challenge)
        if not user_challenge.completed:
            user_challenge.completed = True
            user_challenge.score = challenge.points
            user_challenge.completed_at = timezone.now()
            user_challenge.save()

            # Actualizar puntos y nivel del usuario
            user.points += challenge.points
            user.level = user.points // 100 + 1
            user.save()

        return JsonResponse({
            "success": True,
            "new_points": user.points,
            "new_level": user.level
        })

    except Exception as e:
        print("Error completando reto:", e)
        return JsonResponse({"success": False, "message": str(e)})
