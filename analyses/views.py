from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from config import settings
from users.models import User
from users.serializers import UserSerializer


class AnalysesList(APIView):
    @method_decorator(permission_required("users.read_analysis", raise_exception=True))
    def get(self, request, format=None):
        """
        List instances
        """
        response = requests.get(settings.API_ANALYSES_URL)

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        analyses = response.json()

        sample_ids = list(map(lambda analysis: analysis.get("sample"), analyses))
        response = requests.post(f"{settings.API_SAMPLES_URL}/bulk", json=sample_ids)

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        samples = response.json()

        # traverse through sample users to get correct user object
        analyses = list(
            map(
                lambda analysis: {
                    **analysis,
                    "sample": next(
                        sample
                        for sample in samples
                        if sample.get("id") == analysis.get("sample")
                    ),
                },
                analyses,
            )
        )

        return Response(
            data={"data": analyses, "success": True}, status=response.status_code
        )

    @method_decorator(
        permission_required("users.create_analysis", raise_exception=True)
    )
    def post(self, request, format=None):
        """
        Create new instance
        """
        response = requests.post(
            f"{settings.API_ANALYSES_URL}/",
            {
                "sample": request.data.get("sample"),
                "laborant": request.data.get("laborant"),
                "lab": request.data.get("lab"),
                "tools": request.data.get("tools"),
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


class AnalysisDetail(APIView):
    @method_decorator(permission_required("users.read_analysis", raise_exception=True))
    def get(self, request, id, format=None):
        """
        Get single instance
        """
        response = requests.get(f"{settings.API_ANALYSES_URL}/{id}")

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        analysis = response.json()

        # fetch sample
        response = requests.get(f"{settings.API_SAMPLES_URL}/{analysis.get('sample')}")

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        sample = response.json()
        analysis["sample"] = sample

        # fetch user
        laborant_exists = analysis.get("laborant") is not None
        if laborant_exists:
            user = UserSerializer(User.objects.get(pk=analysis.get("laborant")))
            analysis["laborant"] = user.data

        # fetch lab
        response = requests.get(f"{settings.API_LABS_URL}/{analysis.get('lab')}")

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        lab = response.json()
        analysis["lab"] = lab

        # fetch tools
        response = requests.post(
            f"{settings.API_TOOLS_URL}/bulk", json=analysis.get("tools")
        )

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        tools = response.json()
        analysis["tools"] = tools

        return Response(
            data={
                "data": analysis,
                "success": True,
            },
            status=response.status_code,
        )

    @method_decorator(
        permission_required("users.update_analysis", raise_exception=True)
    )
    def put(self, request, id, format=None):
        """
        Update instance
        """
        response = requests.put(
            f"{settings.API_ANALYSES_URL}/{id}",
            {
                "lab": request.data.get("lab"),
                "laborant": request.data.get("laborant"),
                "sample": request.data.get("sample"),
                "structure": request.data.get("structure", None),
                "tools": request.data.get("tools"),
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

    @method_decorator(
        permission_required("users.delete_analysis", raise_exception=True)
    )
    def delete(self, request, id, format=None):
        """
        Delete instance
        """

        response = requests.delete(f"{settings.API_ANALYSES_URL}/{id}")

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        return Response(data={"success": True}, status=response.status_code)


class AnalysisStart(APIView):
    """
    Analysis start
    """

    @method_decorator(
        permission_required("users.update_analysis", raise_exception=True)
    )
    def post(self, request, id, format=None):
        """
        Update instance
        """
        response = requests.post(
            f"{settings.API_ANALYSES_URL}/{id}/start",
        )

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        return Response(
            data={"data": response.json(), "success": True}, status=response.status_code
        )


class AnalysisFinish(APIView):
    """
    Analysis finish
    """

    @method_decorator(
        permission_required("users.update_analysis", raise_exception=True)
    )
    def post(self, request, id, format=None):
        """
        Update instance
        """
        response = requests.post(
            f"{settings.API_ANALYSES_URL}/{id}/finish",
        )

        if not response.ok:
            return Response(
                data={"errors": response.json(), "success": False},
                status=response.status_code,
            )

        return Response(
            data={"data": response.json(), "success": True}, status=response.status_code
        )
