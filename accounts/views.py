from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


# =========================
# DJANGO URLS -> REDIRECT TO REACT CABINET
# =========================

def register(request):
    # старий /register/ тепер веде в React
    return redirect("/cabinet/register")


def login_view(request):
    # старий /login/ тепер веде в React
    return redirect("/cabinet/login")


def logout_view(request):
    # якщо колись використовувалась django-сесія — очистимо
    logout(request)
    return redirect("/cabinet/login")


def profile(request):
    # /profile/ тепер веде в кабінет
    return redirect("/cabinet")


def cabinet(request):
    return render(request, "cabinet/index.html")



# =========================
# API FOR REACT (JWT)
# =========================

@api_view(["POST"])
@permission_classes([AllowAny])
def api_register(request):
    """
    POST /api/auth/register/
    body: { "username": "...", "password": "...", "email": "..." }
    """
    username = (request.data.get("username") or "").strip()
    password = request.data.get("password") or ""
    email = (request.data.get("email") or "").strip()

    if not username or not password:
        return Response(
            {"detail": "username та password обовʼязкові"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"detail": "Користувач вже існує"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, password=password, email=email)

    return Response(
        {"id": user.id, "username": user.username},
        status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_me(request):
    """
    GET /api/users/me/
    Header: Authorization: Bearer <access_token>
    """
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })
