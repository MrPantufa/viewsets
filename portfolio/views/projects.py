from rest_framework import viewsets
from ..models import Project
from ..serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related("tags","technologies","links").order_by("title")
    serializer_class = ProjectSerializer
