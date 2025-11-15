from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
import json

# === Cargar variables de entorno ===
load_dotenv("openAI.env")

OPENAI_API_KEY = os.getenv("openai_apikey")
HF_API_KEY = os.getenv("hf_api_key")

# === Inicializar cliente de OpenAI ===
client = None
if OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        print("✅ Cliente OpenAI inicializado correctamente.")
    except Exception as e:
        print(f"⚠️ No se pudo inicializar OpenAI: {e}")
else:
    print("⚠️ No se encontró 'openai_apikey' en openAI.env")


# === Función principal ===
def get_completion(prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.6) -> str:
    """
    Envía un prompt a OpenAI; si hay error de cuota o clave, usa Hugging Face como respaldo.
    """
    if client:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            error_text = str(e)
            print(f"⚠️ Error OpenAI: {error_text}")

            # Fallback automático si falla OpenAI
            if "insufficient_quota" in error_text or "401" in error_text or "429" in error_text:
                print("🔄 Cambiando a modelo de respaldo Hugging Face...")
                return get_completion_hf(prompt)
            else:
                return f"⚠️ Error al comunicarse con OpenAI: {e}"

    # Si no hay cliente OpenAI activo
    print("🔄 No hay cliente OpenAI activo. Usando Hugging Face...")
    return get_completion_hf(prompt)


# === Respaldo Hugging Face (router oficial) ===
def get_completion_hf(prompt: str) -> str:
    """
    Usa la API Router de Hugging Face con el modelo Llama 3.1 8B Instruct.
    """
    if not HF_API_KEY:
        return "⚠️ No hay clave de Hugging Face configurada en openAI.env."

    url = "https://router.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 512
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=90)

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        else:
            return f"⚠️ Error Hugging Face ({response.status_code}): {response.text}"

    except Exception as e:
        return f"⚠️ No se pudo conectar con Hugging Face: {e}"


# === Limpieza de Markdown ===
import re

def clean_markdown(text: str) -> str:
    """
    Elimina formato Markdown (**, *, -, etc.) y deja texto plano limpio.
    """
    text = re.sub(r"(\*\*|\*)", "", text)
    text = re.sub(r"(?m)^\s*-\s*", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"#{1,6}\s*", "", text)  # elimina encabezados tipo # Título
    text = re.sub(r">+\s*", "", text)      # elimina citas tipo > texto
    text = text.replace("•", "")
    return text.strip()


# === Funciones específicas ===

def chat_with_ai(message: str) -> str:
    """
    Chat natural con tono profesional y empático.
    """
    prompt = f"Responde de forma natural, profesional y amable al siguiente mensaje:\n\n{message}"
    response = get_completion(prompt, temperature=0.7)
    return clean_markdown(response)


import re

import re

def generate_text(input_text: str, mode: str) -> str:
    """
    Generador de texto limpio y profesional.
    Elimina símbolos Markdown y listas para que siempre sea texto plano.
    """
    if mode == "resumen":
        prompt_base = f"Resume el siguiente texto de manera clara y concisa:\n\n{input_text}"
    elif mode == "mejora":
        prompt_base = f"Mejora la redacción del siguiente texto, manteniendo claridad y profesionalismo:\n\n{input_text}"
    elif mode == "descripcion":
        prompt_base = f"""
Genera una descripción profesional y clara para una vacante basada en la siguiente información:

{input_text}

Instrucciones:
- Devuelve texto limpio y legible, sin Markdown ni símbolos.
- Organiza en subtítulos claros y párrafos separados.
- Mantén estilo natural y profesional.
"""
    else:
        prompt_base = f"Analiza el siguiente texto y devuelve una interpretación clara:\n\n{input_text}"

    # Llamada al modelo
    texto_generado = get_completion(prompt_base, temperature=0.6)

    # === Postprocesamiento avanzado ===
    texto_limpio = clean_markdown(texto_generado)
    return texto_limpio.strip()




def recommend_vacancies(user_info: str) -> str:
    """
    Recomendador de vacantes o retos personalizados.
    """
    prompt = f"""
    El usuario describe su perfil profesional así:
    {user_info}

    Basándote en ello, sugiere 3 vacantes o retos que encajen con sus habilidades,
    explicando brevemente por qué podrían interesarle. Usa formato numerado y tono profesional.
    """
    response = get_completion(prompt, temperature=0.8)
    return clean_markdown(response)
