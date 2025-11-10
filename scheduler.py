import os
import django
import schedule
import time
from datetime import datetime
from django.core.mail import send_mail

# --- Configura el entorno Django ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streak_project.settings')
django.setup()

# Importa tu modelo de usuario personalizado
from users.models import User  

def send_daily_email():
    """Envía un correo a todos los usuarios registrados invitándolos a volver a la app."""
    users = User.objects.all()

    if not users:
        print(f"[{datetime.now()}] ⚠️ No hay usuarios registrados.")
        return

    for user in users:
        if not user.email:
            continue  # omite usuarios sin correo

        subject = "¡Vuelve hoy a Streak! 🎯"
        message = (
            f"Hola {user.first_name or user.username},\n\n"
            "Hay nuevas vacantes y retos esperándote hoy en Streak.\n"
            "¡Entra ahora y sigue mejorando tu progreso diario!\n\n"
            "👉 https://streak.com\n\n"
            "— El equipo de Streak 💪"
        )

        try:
            send_mail(
                subject,
                message,
                os.getenv("DEFAULT_FROM_EMAIL"),  # correo verificado en SendGrid
                [user.email],
                fail_silently=False,
            )
            print(f"[{datetime.now()}] ✅ Correo enviado a {user.email}")
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Error al enviar a {user.email}: {e}")

# --- Programar el envío diario ---
schedule.every().day.at("09:00").do(send_daily_email)



print("📬 Scheduler de correos iniciado...")

# --- Bucle principal ---
while True:
    schedule.run_pending()
    time.sleep(60)
