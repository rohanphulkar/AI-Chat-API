from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Profile,Purchase
from .serializers import ProfileSerializer,PurchaseSerializer
from rest_framework.permissions import IsAuthenticated
import stripe
from decouple import config
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone

stripe.api_key=config("STRIPE_API_KEY")

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        purchase = Purchase.objects.create(user=request.user)
        checkout_session = stripe.checkout.Session.create(
                    line_items=[
                            {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                            'name': f"Professional Plan",
                            },
                            'unit_amount': int(5 * 100),
                        },
                        'quantity': 1,
                    }
                    ],
                    mode='payment',
                    success_url=settings.FRONTEND_URL+f"/payment-success/{str(purchase.id)}",
                    cancel_url=settings.FRONTEND_URL+f"/payment-failed/{str(purchase.id)}"
                )
        purchase.payment_id=checkout_session.id
        purchase.save()
        return redirect(checkout_session.url)

class PaymentVerifyView(APIView):
    def post(self, request,id):
        try:
            purchase =  Purchase.objects.get(id=id)
        except Purchase.DoesNotExist:
            return Response({'error':'invalid payment id'},status=status.HTTP_400_BAD_REQUEST)
        if purchase.is_paid:
            return Response({'success':'payment successful'},status=status.HTTP_200_OK)
        charges = stripe.checkout.Session.retrieve(purchase.payment_id)
        if charges.payment_status !="paid":
            return Response({'error':'payment failed'},status=status.HTTP_400_BAD_REQUEST)
        purchase.is_paid = True
        purchase.plan_validity = timezone.now() + timezone.timedelta(days=30)
        purchase.save()
        return Response({'success':'payment successful'},status=status.HTTP_200_OK)