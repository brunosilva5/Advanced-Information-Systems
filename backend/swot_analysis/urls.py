from .views import SWOTAnalysisViewSet, QuadrantViewSet, FactorViewSet

# from rest_framework.routers import DefaultRouter

# # router = DefaultRouter()
# # router.register(r"", SWOTAnalysisViewset, basename="swot_analysis")

# # urlpatterns = router.urls
# urlpatterns = [
#     path("", SWOTAnalysisView.as_view(), name="create_client"),
# # Create client
# ]

from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(
    r"swot_analyses",
    SWOTAnalysisViewSet,
    basename="swot_analyses",
)


analysis_router = routers.NestedSimpleRouter(
    router, r"swot_analyses", lookup="swot_analysis"
)
analysis_router.register(
    r"quadrants",
    QuadrantViewSet,
    basename="quadrants",
)


quadrants_router = routers.NestedSimpleRouter(
    analysis_router,
    r"quadrants",
    lookup="quadrant",
)
quadrants_router.register(
    r"factors",
    FactorViewSet,
    basename="factors",
)


urlpatterns = router.urls + analysis_router.urls + quadrants_router.urls
