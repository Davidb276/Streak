from django.core.mail import send_mail
from django.utils import timezone
from users.models import User

def enviar_recordatorios():
    """
    Envía un correo de recordatorio a los usuarios activos.
    """
    usuarios = User.objects.filter(is_active=True)
    for usuario in usuarios:
        send_mail(
            subject="¡Vuelve a Streak!",
            message=f"Hola {usuario.username}, te extrañamos en Streak. ¡Vuelve a completar tus retos hoy!",
            from_email="davidrees035@gmail.com",
            recipient_list=[usuario.email],
            fail_silently=False,
        )
    print("✅ Recordatorios enviados correctamente.")
