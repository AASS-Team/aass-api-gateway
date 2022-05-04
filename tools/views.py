from rest_framework.views import APIView
from rest_framework.response import Response

from config import settings
import requests


class ToolsList(APIView):
    def get(self, request, format=None):
        """
        List instances
        """
        response = requests.get(settings.API_TOOLS_URL)

        if not response.ok:
            return Response(
                {"error": response.reason, "success": False},
                status=response.status_code,
            )

        return Response(
            {"data": response.json(), "success": True}, status=response.status_code
        )

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
                {"error": response.reason, "success": False},
                status=response.status_code,
            )

        return Response(
            {"data": response.json(), "success": True}, status=response.status_code
        )


class ToolDetail(APIView):
    def get(self, request, id, format=None):
        """
        Get single instance
        """
        response = requests.get(f"{settings.API_TOOLS_URL}/{id}")

        if not response.ok:
            return Response(
                {"error": response.reason, "success": False},
                status=response.status_code,
            )

        return Response(
            {"data": response.json(), "success": True}, status=response.status_code
        )

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
                {"error": response.reason, "success": False},
                status=response.status_code,
            )

        return Response(
            {"data": response.json(), "success": True}, status=response.status_code
        )

    def delete(self, request, id, format=None):
        """
        Delete instance
        """
        response = requests.delete(f"{settings.API_TOOLS_URL}/{id}")

        if not response.ok:
            return Response(
                {"error": response.reason, "success": False},
                status=response.status_code,
            )

        return Response({"success": True}, status=response.status_code)
