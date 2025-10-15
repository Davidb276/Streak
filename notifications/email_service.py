# notifications/email_service.py
from django.core.mail import send_mail

def enviar_notificacion(email, asunto, mensaje):
    send_mail(
        asunto,
        mensaje,
        'no-reply@streak.com',
        [email],
        fail_silently=False,
    )
