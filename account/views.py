import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, UserDetails
from twilio.rest import Client
from django.conf import settings
from .serializers import CustomUserSerializer, UserDetailsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def send_otp_via_sms(mobile_number, otp):
    # Generate a random OTP (6 digits)
    # otp = ''.join(random.choices('0123456789', k=4))

    # Initialize the Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Send the OTP via SMS
    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=mobile_number
    )

    return otp


class SendOTPAPI(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        mobile_number = request.data.get('mobile_number')
        email = request.data.get("email")
        user, created = CustomUser.objects.get_or_create(mobile_number=mobile_number, email=email)
        user.is_verified = False
        if created or not user.is_verified:
            # email_data.save()
            otp = str(random.randint(1000, 9999))
            user.otp = otp
            user.save()
            send_otp_via_sms(mobile_number, otp)
            # return Response({'data': "Otp Sent Successfully"}, status=status.HTTP_200_OK)
            return Response({'data': {"mobile_number": mobile_number, "otp": otp}}, status=status.HTTP_200_OK)
        return Response({'message': 'Mobile number is already verified'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPAPI(APIView):
    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        otp = request.data.get('otp')
        try:
            # import pdb; pdb.set_trace()
            user = CustomUser.objects.get(mobile_number=mobile_number, otp=otp, is_verified=False)
            user.is_verified = True
            user.save()
            token = get_tokens_for_user(user)
            return Response({'message': 'Mobile number verified successfully', "token": token},
                            status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Invalid OTP or mobile number'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsViewSet(ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
