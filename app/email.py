from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Message
from app import app,mail

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    
def envia_pass_correo(user):
    token = user.get_reset_token()
    send_email('Restablece tu contraseña',
    sender = app.config['MAIL_USERNAME'][0],
    recipients = [user.email],
    text_body = render_template('email/reset_password.txt', user=user, token=token),
    html_body = render_template('email/reset_password.html', user=user, token=token))
