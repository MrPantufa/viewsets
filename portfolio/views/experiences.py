from rest_framework import viewsets
from ..models import Experience
from ..serializers import ExperienceSerializer

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all().order_by("-started_at")
    serializer_class = ExperienceSerializer
