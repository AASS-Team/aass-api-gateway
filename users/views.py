from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import Group
from .models import User
from . import serializers


class UsersList(APIView):
    serializer_class = serializers.UserSerializer

    @method_decorator(permission_required("users.read_user", raise_exception=True))
    def get(self, request, format=None):
        """
        List instances
        """
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)

        return Response(
            data={"data": serializer.data, "success": True}, status=status.HTTP_200_OK
        )

    @method_decorator(permission_required("users.create_user", raise_exception=True))
    def post(self, request, format=None):
        """
        Create new instance
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={"errors": serializer.errors, "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            data={"data": serializer.data, "success": True},
            status=status.HTTP_201_CREATED,
        )


class UserDetail(APIView):
    def get_object(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise NotFound()

    @method_decorator(permission_required("users.read_user", raise_exception=True))
    def get(self, request, id, format=None):
        """
        Get single instance
        """
        user = self.get_object(id)
        serializer = serializers.UserSerializer(user)
        return Response(
            data={"data": serializer.data, "success": True}, status=status.HTTP_200_OK
        )

    @method_decorator(permission_required("users.update_user", raise_exception=True))
    def put(self, request, id, format=None):
        """
        Update instance
        """
        user = self.get_object(id)
        serializer = serializers.UserSerializer(user, data=request.data)

        if not serializer.is_valid():
            return Response(
                data={"errors": serializer.errors, "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            data={"data": serializer.data, "success": True}, status=status.HTTP_200_OK
        )

    @method_decorator(permission_required("users.delete_user", raise_exception=True))
    def delete(self, request, id, format=None):
        """
        Delete instance
        """
        user = self.get_object(id)
        deleted_rows = user.delete()

        if len(deleted_rows) <= 0:
            return Response(
                data={"errors": ["Internal server error"], "success": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data={"success": True}, status=status.HTTP_204_NO_CONTENT)


class GroupsList(APIView):
    serializer_class = serializers.GroupSerializer

    @method_decorator(permission_required("users.read_group", raise_exception=True))
    def get(self, request, format=None):
        """
        List instances
        """
        groups = Group.objects.all()
        serializer = self.serializer_class(groups, many=True)

        return Response(
            data={"data": serializer.data, "success": True}, status=status.HTTP_200_OK
        )


class UserPermissionsList(APIView):
    serializer_class = serializers.PermissionSerializer

    @method_decorator(
        permission_required("users.read_permission", raise_exception=True)
    )
    def get(self, request, format=None):
        """
        List instances
        """
        permissions = request.user.user_permissions.all().values_list(
            "codename", flat=True
        )
        serializer = self.serializer_class(permissions, many=True)

        return Response(
            data={"data": serializer.data, "success": True}, status=status.HTTP_200_OK
        )
