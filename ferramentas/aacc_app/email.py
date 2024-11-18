from django.core.mail import send_mail
from django.conf import settings

def send_activity_assignment_email(professor_email, activity_details):
    subject = 'Nova Atividade Atribuída para Avaliação'
    message = f'Você tem uma nova atividade esperando sua avaliação. Detalhes: {activity_details}'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [professor_email]
    send_mail(subject, message, email_from, recipient_list)
    