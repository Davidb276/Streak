from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
import random, re
from ai_module.openai_client import generate_text
from .models import Challenge, UserChallenge

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

    # Inicializar sesión para retos generados
    if "retos_generados" not in request.session:
        request.session["retos_generados"] = []

    # Generar retos nuevos
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
        retos_generados = re.sub(r'(?i)(vacante|proyecto|rol|introducción|objetivo):.*$', '', retos_generados, flags=re.MULTILINE)
        bloques = re.split(r'(?=Reto\s*\d*[:\-]|Desaf[ií]o\s*\d*[:\-])', retos_generados, flags=re.IGNORECASE)
        retos_limpios = [b.strip() for b in bloques if b.strip().lower().startswith(("reto", "desaf"))]

        # Guardar en sesión
        request.session["retos_generados"] = []
        for idx, bloque in enumerate(retos_limpios[:3]):
            lineas = bloque.split("\n", 1)
            titulo = lineas[0].strip()
            descripcion = lineas[1].strip() if len(lineas) > 1 else "Descripción no disponible."
            request.session["retos_generados"].append({
                "session_id": str(idx),
                "titulo": titulo,
                "descripcion": descripcion
            })
        request.session.modified = True

    retos = request.session.get("retos_generados", [])
    retos_completados = UserChallenge.objects.filter(user=user, completed=True)

    return render(request, "challenges/challenge_list.html", {
        "user_data": user_data,
        "retos": retos,
        "retos_completados": retos_completados
    })


@login_required
def completar_reto(request, session_id):
    user = request.user
    retos = request.session.get("retos_generados", [])
    reto = next((r for r in retos if r["session_id"] == session_id), None)
    if not reto:
        return JsonResponse({"success": False})

    try:
        puntos_por_reto = 10
        user.points += puntos_por_reto
        user.level = user.points // 100 + 1
        user.save()

        # Guardar reto completado en DB
        ch, _ = Challenge.objects.get_or_create(title=reto["titulo"], defaults={"description": reto["descripcion"], "points": puntos_por_reto})
        UserChallenge.objects.get_or_create(user=user, challenge=ch, defaults={
            "completed": True,
            "score": puntos_por_reto,
            "completed_at": timezone.now()
        })

        return JsonResponse({
            "success": True,
            "new_points": user.points,
            "new_level": user.level
        })
    except Exception as e:
        print("Error completando reto:", e)
        return JsonResponse({"success": False})
