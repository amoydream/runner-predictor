from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from api import serializers
from rest_framework import status
from api.models import Runner, RaceResult


class RunnerViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """Manage Race in the database"""

    queryset = Runner.objects.all()
    serializer_class = serializers.RunnerSerializer


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
