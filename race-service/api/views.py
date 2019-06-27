from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from api import serializers
from rest_framework import status
from rest_framework.decorators import action
from api.models import Race, RaceResult, RaceGroup


class RaceGroupViewSet(viewsets.ModelViewSet):
    queryset = RaceGroup.objects.all()
    serializer_class = serializers.RaceGroupSerializer


class RaceViewSet(NestedViewSetMixin, viewsets.ModelViewSet):

    queryset = Race.objects.all()
    serializer_class = serializers.RaceSerializer

    @action(detail=False, methods=["post"])
    def download_enduhub_data(self, request):
        race = Race.objects.get(pk=request.data["race_id"])
        race.download_from_enduhub()
        return Response("Send to download", status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def download_itra_data(self, request):
        race = Race.objects.get(pk=request.data["race_id"])
        race.download_from_itra()
        return Response("Send to download", status=status.HTTP_201_CREATED)


class RaceResultViewSet(NestedViewSetMixin, viewsets.ModelViewSet):

    queryset = RaceResult.objects.all()
    serializer_class = serializers.RaceResultSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["race"] = kwargs.get("parent_lookup_race")
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
