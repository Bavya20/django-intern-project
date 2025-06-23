from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# ✅ Add RegisterUser import here
from api.views import RegisterUser, PublicAPIView, ProtectedAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔐 Login page (HTML form)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # 🌐 Public and Protected API
    path('public/', PublicAPIView.as_view(), name='public-api'),
    path('protected/', ProtectedAPIView.as_view(), name='protected-api'),

    # 🔑 JWT Token Authentication
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    # 📝 Registration endpoint for new users
    path('register/', RegisterUser.as_view(), name='register'),
]
