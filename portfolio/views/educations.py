from rest_framework import viewsets
from ..models import Education
from ..serializers import EducationSerializer

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all().order_by("-started_at")
    serializer_class = EducationSerializer
