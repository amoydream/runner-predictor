from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin
from api import views


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()
(
    router.register("runners", views.RunnerViewSet).register(
        "race_results",
        views.RaceResultViewSet,
        basename="race-results",
        parents_query_lookups=["runner"],
    )
)


app_name = "api"

urlpatterns = [path("", include(router.urls))]
