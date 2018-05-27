from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics
from .serializers import *
from .models import *


class DataCreateView(generics.CreateAPIView):
    """
    View to create Data Object only by super admin
    """
    permission_classes = [IsAdminUser]
    serializer_class = DataSerializer
    lookup_field = "pk"
    queryset = Data.objects.all()
    name = "create"


class DataListView(generics.ListAPIView):
    """
    View to List Data Object
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DataSerializer
    lookup_field = "pk"
    queryset = Data.objects.all()
    name = "list"


class DataRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieve, update , delete of Data objects only by superuser
    """
    permission_classes = [IsAdminUser]
    serializer_class = DataSerializer
    lookup_field = "pk"
    queryset = Data.objects.all()
    name = "data_rud"
