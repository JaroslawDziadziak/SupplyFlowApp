from django.contrib import admin
from django.urls import path, include

# Import the two JWT views:
# - TokenObtainPairView: POST /api/token/ → returns access + refresh token
# - TokenRefreshView: POST /api/token/refresh/ → returns a new access token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints (tickets, comments)
    path('api/', include('tickets.urls')),

    # JWT Authentication endpoints
    # POST /api/token/ → send username+password, receive tokens
    # POST /api/token/refresh/ → send refresh token, receive new access token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
