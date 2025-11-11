from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from .openai_client import get_completion  # Usa tu cliente existente


# 💬 CHAT INTERACTIVO
@csrf_exempt
def chat_view(request):
    """
    Vista del chat con IA (AJAX).
    Limpia el formato Markdown (**texto**, *texto*, listas, etc.)
    y mantiene el prefijo "IA:" con texto plano.
    """
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()
        if not user_message:
            return JsonResponse({"response": "⚠️ Por favor escribe algo antes de enviar."})

        # Prompt para el modelo
        prompt = f"Responde de forma conversacional y profesional a este mensaje:\n{user_message}"
        raw_response = get_completion(prompt)

        # 🔹 Limpiar formato Markdown y símbolos
        clean_response = re.sub(r"\*\*(.*?)\*\*", r"\1", raw_response)   # quitar **negritas**
        clean_response = re.sub(r"\*(.*?)\*", r"\1", clean_response)     # quitar *cursivas*
        clean_response = re.sub(r"\d+\.\s*", "", clean_response)         # quitar "1. ", "2. ", etc.
        clean_response = re.sub(r"[-•]\s*", "", clean_response)          # quitar viñetas
        clean_response = re.sub(r"\n+", "\n", clean_response)            # normalizar saltos de línea
        clean_response = clean_response.strip()

        # Asegurar prefijo "IA:"
        if not clean_response.startswith("IA:"):
            clean_response = f"IA: {clean_response}"

        return JsonResponse({"response": clean_response})

    # Si es GET, renderiza el HTML del chat
    return render(request, "ai_module/chat.html")


# ✍️ GENERADOR / ANALIZADOR DE TEXTO
def generator_view(request):
    """
    Vista que permite resumir, mejorar o generar texto según el modo seleccionado.
    """
    context = {}
    if request.method == "POST":
        input_text = request.POST.get("input_text", "").strip()
        mode = request.POST.get("mode", "resumen")

        if not input_text:
            context["error"] = "Por favor ingresa un texto válido."
        else:
            if mode == "resumen":
                prompt = f"Resume el siguiente texto en pocas frases claras y precisas:\n\n{input_text}"
            elif mode == "mejora":
                prompt = f"Mejora la redacción del siguiente texto manteniendo su sentido y tono profesional:\n\n{input_text}"
            elif mode == "descripcion":
                prompt = f"Genera una descripción atractiva para una vacante basada en:\n\n{input_text}"
            else:
                prompt = input_text

            response = get_completion(prompt)
            context = {"input_text": input_text, "response": response, "mode": mode}

    return render(request, "ai_module/generator.html", context)


# 🎯 RECOMENDADOR DE VACANTES / RETOS
def recommender_view(request):
    """
    Vista que genera recomendaciones personalizadas de vacantes o retos
    basadas en las habilidades o intereses del usuario.
    """
    context = {}
    if request.method == "POST":
        user_info = request.POST.get("user_info", "").strip()

        if not user_info:
            context["error"] = "Por favor describe tus habilidades o intereses."
        else:
            prompt = f"""
            El usuario describe su perfil profesional así:
            {user_info}

            Basándote en esto, recomienda 3 posibles vacantes o retos adecuados a su perfil,
            explicando brevemente por qué encajan con sus habilidades.
            """
            response = get_completion(prompt)
            context = {"user_info": user_info, "response": response}

    return render(request, "ai_module/recommender.html", context)
