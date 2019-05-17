from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin
from api import views


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()
(
    router.register("races", views.RaceViewSet).register(
        "race_results",
        views.RaceResultViewSet,
        basename="race-results",
        parents_query_lookups=["race"],
    )
)


app_name = "api"

urlpatterns = [path("", include(router.urls))]
