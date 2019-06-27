from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import (
    NestedViewSetMixin,
    DetailSerializerMixin,
)
from rest_framework.decorators import action
from api import serializers
from rest_framework import status
from api.models import Runner, RaceResult


class RunnerViewSet(
    DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet
):
    """Manage runner in the database"""

    queryset = Runner.objects.all()
    serializer_class = serializers.RunnerSerializer
    serializer_detail_class = serializers.RunnerSerializer
    filterset_fields = ("name", "birth_year")

    @action(detail=False, methods=["post"])
    def get_or_create(self, request):
        if not request.data["birth_year"].isnumeric():
            return Response(
                "Birth year is wrong format",
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            runner = Runner.objects.get(
                name=request.data["name"],
                birth_year=request.data["birth_year"],
            )
            serializer = serializers.RunnerSerializer(
                runner, context={"request": request}
            )
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_200_OK, headers=headers
            )
        except ObjectDoesNotExist:
            serializer = serializers.RunnerSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )


class RaceResultViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """Manage RaceResult in the database"""

    queryset = RaceResult.objects.all()
    serializer_class = serializers.RaceResultSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["runner"] = kwargs.get("parent_lookup_runner")
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
