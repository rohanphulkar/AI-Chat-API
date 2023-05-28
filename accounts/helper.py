from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(email,link):
    try:
        subject = "Account Verification"
        body =  f"Dear {email},\n\nplease verify your account by clicking the link:\n\n{link}\n\nThank you!"
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [email]
        )

        return True
    except Exception as e:
        return False
    

def send_password_reset_email(email,link):
    try:
        subject = "Password reset request"
        body = f"You can reset your password by clicking the link below.\n\n{link}\n\nThank you!"
        send_mail(subject,body,settings.EMAIL_HOST_USER,[email])
        return True
    except Exception as e:
        return False