from rest_framework import viewsets
from ..models import ProjectLink
from ..serializers import ProjectLinkSerializer

class ProjectLinkViewSet(viewsets.ModelViewSet):
    queryset = ProjectLink.objects.select_related("project").all().order_by("label")
    serializer_class = ProjectLinkSerializer
