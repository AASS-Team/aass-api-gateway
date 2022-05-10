from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from config import settings
from users.models import User
from users.serializers import UserSerializer


class SamplesList(APIView):
    def get(self, request, format=None):
        """
        List instances
        """
        response = requests.get(settings.API_SAMPLES_URL)

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        samples = response.json()

        user_ids = list(map(lambda sample: sample["user"], samples))
        users = UserSerializer(User.objects.filter(Q(id__in=user_ids)), many=True).data

        # traverse through sample users to get correct user object
        samples = list(
            map(
                lambda sample: {
                    **sample,
                    "user": next(
                        user for user in users if user["id"] == sample["user"]
                    ),
                },
                samples,
            )
        )

        return Response(
            data={"data": samples, "success": True}, status=response.status_code
        )

    def post(self, request, format=None):
        """
        Create new instance
        """
        response = requests.post(
            f"{settings.API_SAMPLES_URL}/",
            {
                "name": request.data.get("name"),
                "amount": request.data.get("amount"),
                "note": request.data.get("note", None),
                "user": request.data.get("user"),
                "grant": request.data.get("grant"),
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


class SampleDetail(APIView):
    def get(self, request, id, format=None):
        """
        Get single instance
        """
        response = requests.get(f"{settings.API_SAMPLES_URL}/{id}")

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        sample = response.json()

        # fetch grant
        grant_exists = sample["grant"] is not None
        if grant_exists:
            grant = requests.get(f"{settings.API_GRANTS_URL}/{sample['grant']}")

        # get user
        user = UserSerializer(User.objects.get(pk=sample["user"]))

        return Response(
            data={
                "data": {
                    **sample,
                    "user": user.data,
                    "grant": grant.json() if grant_exists else None,
                },
                "success": True,
            },
            status=response.status_code,
        )

    def put(self, request, id, format=None):
        """
        Update instance
        """
        response = requests.put(
            f"{settings.API_SAMPLES_URL}/{id}",
            {
                "name": request.data.get("name"),
                "amount": request.data.get("amount"),
                "note": request.data.get("note", None),
                "user": request.data.get("user"),
                "grant": request.data.get("grant"),
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
        response = requests.delete(f"{settings.API_SAMPLES_URL}/{id}")

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        return Response(data={"success": True}, status=response.status_code)
