from django.urls import path, include
from .authentication.views import (
    ProfileView,
    ObtainTokenPairView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('sign_up/', ProfileView.as_view({'post': 'create'})),
    path('token/', ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
]
