from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from config import settings


class ToolsList(APIView):
    @method_decorator(permission_required("users.read_tool", raise_exception=True))
    def get(self, request, format=None):
        """
        List instances
        """
        response = requests.get(settings.API_TOOLS_URL)

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        return Response(
            data={"data": response.json(), "success": True}, status=response.status_code
        )

    @method_decorator(permission_required("users.create_tool", raise_exception=True))
    def post(self, request, format=None):
        """
        Create new instance
        """
        response = requests.post(
            f"{settings.API_TOOLS_URL}/",
            {"name": request.data["name"], "type": request.data["type"]},
        )

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        return Response(
            data={"data": response.json(), "success": True}, status=response.status_code
        )


class ToolDetail(APIView):
    @method_decorator(permission_required("users.read_tool", raise_exception=True))
    def get(self, request, id, format=None):
        """
        Get single instance
        """
        response = requests.get(f"{settings.API_TOOLS_URL}/{id}")

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        return Response(
            data={"data": response.json(), "success": True}, status=response.status_code
        )

    @method_decorator(permission_required("users.update_tool", raise_exception=True))
    def put(self, request, id, format=None):
        """
        Update instance
        """
        response = requests.put(
            f"{settings.API_TOOLS_URL}/{id}",
            {
                "name": request.data["name"],
                "type": request.data["type"],
            },
        )

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        return Response(
            data={"data": response.json(), "success": True}, status=response.status_code
        )

    @method_decorator(permission_required("users.delete_tool", raise_exception=True))
    def delete(self, request, id, format=None):
        """
        Delete instance
        """
        response = requests.delete(f"{settings.API_TOOLS_URL}/{id}")

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        return Response(data={"success": True}, status=response.status_code)
