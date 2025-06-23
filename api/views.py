from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .tasks import send_welcome_email

# ✅ User Registration API
class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if not all([username, password, email]):
            return Response({"error": "All fields are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken."}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)

        # ✅ Send email in background
        send_welcome_email.delay(user.email)

        return Response({"message": "User registered successfully!"}, status=201)


# ✅ Public API
class PublicAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Hello, this is a public endpoint!"})


# ✅ Protected API
class ProtectedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}. This is a protected endpoint!"})
