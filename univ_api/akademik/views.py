from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters import rest_framework as filters

from .models import Prodi, Siswa, Kuliah, Registrasi
from .serializers import (
    ProdiSerializer, SiswaSerializer, KuliahSerializer, RegistrasiSerializer
)


class SiswaFilter(filters.FilterSet):
    prodi = filters.CharFilter(field_name="prodi__nama", lookup_expr="iexact")

    class Meta:
        model = Siswa
        fields = ["prodi"]


class KuliahFilter(filters.FilterSet):
    prodi = filters.CharFilter(field_name="prodi__nama", lookup_expr="iexact")

    class Meta:
        model = Kuliah
        fields = ["prodi", "hari", "sks"]


class RegistrasiFilter(filters.FilterSet):
    prodi = filters.CharFilter(field_name="kuliah__prodi__nama", lookup_expr="iexact")

    class Meta:
        model = Registrasi
        fields = ["student", "kuliah", "prodi"]


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

class ProdiViewSet(BaseViewSet):
    queryset = Prodi.objects.all().order_by("nama")
    serializer_class = ProdiSerializer
    search_fields = ["nama", "kaprodi"]
    ordering_fields = ["nama"]
    lookup_field = "nama"
    lookup_value_regex = "[^/]+"

class SiswaViewSet(BaseViewSet):
    queryset = Siswa.objects.select_related("prodi").all().order_by("nim")
    serializer_class = SiswaSerializer
    filterset_class = SiswaFilter
    lookup_field = "prodi"
    search_fields = ["nama", "nim"]
    ordering_fields = ["nim", "nama"]

class KuliahViewSet(BaseViewSet):
    queryset = Kuliah.objects.select_related("prodi").all().order_by("matkul")
    serializer_class = KuliahSerializer
    filterset_class = KuliahFilter
    search_fields = ["matkul"]
    ordering_fields = ["matkul", "sks", "hari"]

class RegistrasiViewSet(BaseViewSet):
    queryset = Registrasi.objects.select_related("student", "kuliah").all()
    serializer_class = RegistrasiSerializer
    filterset_class = RegistrasiFilter
    search_fields = ["student__nim", "student__nama", "kuliah__matkul"]
    ordering_fields = ["id"]
