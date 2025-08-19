
from rest_framework import viewsets
from .models import Tag, Technology, Project, ProjectLink, Experience, Education
from .serializers import (
    TagSerializer, TechnologySerializer, ProjectSerializer,
    ProjectLinkSerializer, ExperienceSerializer, EducationSerializer,
)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer

class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all().order_by("name")
    serializer_class = TechnologySerializer

class ProjectLinkViewSet(viewsets.ModelViewSet):
    queryset = ProjectLink.objects.select_related("project").all().order_by("label")
    serializer_class = ProjectLinkSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related("tags","technologies","links").order_by("title")
    serializer_class = ProjectSerializer

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all().order_by("-started_at")
    serializer_class = ExperienceSerializer

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all().order_by("-started_at")
    serializer_class = EducationSerializer
