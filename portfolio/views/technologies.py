from rest_framework import viewsets
from ..models import Technology
from ..serializers import TechnologySerializer

class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all().order_by("name")
    serializer_class = TechnologySerializer
