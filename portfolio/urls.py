
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TagViewSet, TechnologyViewSet, ProjectViewSet,
    ProjectLinkViewSet, ExperienceViewSet, EducationViewSet,
)
router = DefaultRouter()
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"technologies", TechnologyViewSet, basename="technology")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"project-links", ProjectLinkViewSet, basename="projectlink")
router.register(r"experiences", ExperienceViewSet, basename="experience")
router.register(r"educations", EducationViewSet, basename="education")
urlpatterns = [path("", include(router.urls))]
