from rest_framework import filters, generics
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from django.views.generic import TemplateView
from .models import Berita, Komentar
from .serializers import (
    BeritaDetailSerializer,
    BeritaListSerializer,
    KomentarSerializer,
)


class BeritaListView(generics.ListCreateAPIView):
    queryset = Berita.objects.all().order_by("-tanggal")
    filter_backends = [filters.SearchFilter]
    search_fields = ["judul"]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BeritaDetailSerializer
        return BeritaListSerializer


class BeritaDetailView(generics.RetrieveUpdateAPIView):
    queryset = Berita.objects.all()
    serializer_class = BeritaDetailSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]


class KomentarListView(generics.ListCreateAPIView):
    queryset = Komentar.objects.select_related("berita").all().order_by("-tanggal")
    serializer_class = KomentarSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nama", "isi"]
    ordering_fields = ["tanggal", "nama"]


class BeritaDashboardPage(TemplateView):
    template_name = "template.html"


class BeritaDetailPage(TemplateView):
    template_name = "berita-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["berita_id"] = self.kwargs["pk"]
        return context
