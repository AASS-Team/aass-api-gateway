from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import status


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
        Login
        """
        username = request.data.get("username")
        password = request.data.get("password")

        if username is None or password is None:
            return Response(
                data={"errors": ["Please provide both username and password"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                data={"error": "Invalid Credentials"}, status=status.HTTP_404_NOT_FOUND
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={"token": token.key}, status=status.HTTP_200_OK)
