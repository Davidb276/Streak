def generar_recomendaciones(usuario):
    """
    Simula recomendaciones basadas en progreso del usuario.
    En una versión avanzada se conectaría a una API de IA (por ej. OpenAI).
    """
    if usuario.points < 50:
        return ["Completa el reto 'Lógica básica'", "Revisa fundamentos de Python"]
    elif usuario.points < 200:
        return ["Prueba el reto 'Desarrollo Web con Django'", "Aplica a vacantes junior"]
    else:
        return ["Considera vacantes senior", "Comparte tus logros en LinkedIn"]
