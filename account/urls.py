from django.urls import path, include
from account.views import SendOTPAPI, VerifyOTPAPI, UserDetailsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('user-details', UserDetailsViewSet, basename="user_details")

urlpatterns = [
    path('', include(router.urls)),
    path('send-otp/', SendOTPAPI.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPAPI.as_view(), name='verify_otp'),
]
