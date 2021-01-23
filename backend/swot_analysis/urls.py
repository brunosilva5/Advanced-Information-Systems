from django.urls import path

from .views import SWOTAnalysisView

from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r"", SWOTAnalysisViewset, basename="swot_analysis")

# urlpatterns = router.urls
urlpatterns = [
    path("", SWOTAnalysisView.as_view(), name="create_client"),  # Create client
]