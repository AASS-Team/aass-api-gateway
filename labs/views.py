from rest_framework.views import APIView
from rest_framework.response import Response

from config import settings
import requests


class LabsList(APIView):
    def get(self, request, format=None):
        """
        List instances
        """
        response = requests.get(settings.API_LABS_URL)

        if not response.ok:
            return Response(
                {"errors": response.json(), "success": False},
                status=response.status_code,
            )

        return Response(
            data={"data": response.json(), "success": True}, status=response.status_code
        )

    def post(self, request, format=None):
        """
        Create new instance
        """
        response = requests.post(
            f"{settings.API_LABS_URL}/",
            {"name": request.data["name"], "address": request.data["address"]},
        )

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        return Response(
            data={"data": response.json(), "success": True}, status=response.status_code
        )


class LabDetail(APIView):
    def get(self, request, id, format=None):
        """
        Get single instance
        """
        response = requests.get(f"{settings.API_LABS_URL}/{id}")

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        return Response(
            data={"data": response.json(), "success": True}, status=response.status_code
        )

    def put(self, request, id, format=None):
        """
        Update instance
        """
        response = requests.put(
            f"{settings.API_LABS_URL}/{id}",
            {
                "name": request.data["name"],
                "address": request.data["address"],
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

    def delete(self, request, id, format=None):
        """
        Delete instance
        """
        response = requests.delete(f"{settings.API_LABS_URL}/{id}")

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        return Response(data={"success": True}, status=response.status_code)
