from flask import Blueprint, request, jsonify
import smtplib
from email.message import EmailMessage
import os

maintenance_bp = Blueprint('maintenance', __name__, url_prefix='/api/maintenance/messages')

@maintenance_bp.route('/', methods=['POST'])
def send_maintenance_email():
    data = request.json
    sender = data.get('sender')
    content = data.get('content')

    if not sender or not content:
        return jsonify({'error': 'Remetente e conteúdo são obrigatórios.'}), 400

    try:
        msg = EmailMessage()
        msg['Subject'] = 'Nova Notificação de Manutenção'
        msg['From'] = os.environ.get('MAIL_FROM')
        msg['To'] = os.environ.get('MAINTENANCE_TEAM_EMAIL')

        msg.set_content(f"Remetente: {sender}\n\nMensagem:\n{content}")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ.get('MAIL_FROM'), os.environ.get('MAIL_PASSWORD'))
            smtp.send_message(msg)

        return jsonify({'message': 'E-mail enviado com sucesso'}), 200

    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return jsonify({'error': 'Falha ao enviar e-mail'}), 500
