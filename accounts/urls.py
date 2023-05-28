from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("verify/<token>/", EmailVerificationView.as_view(), name="verify"),
    path("login/",LoginView.as_view(), name="login"),
    path("forgot-password/",ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/<token>/",ResetPasswordView.as_view(), name="reset_password"),
    path("change-password/",ChangePasswordView.as_view(), name="change_password"),
]
