from django.urls import path
from .views import ProfileView,CheckoutView

urlpatterns = [
    path("",ProfileView.as_view(), name="profile"),
    path("checkout/",CheckoutView.as_view(), name="checkout"),
]
