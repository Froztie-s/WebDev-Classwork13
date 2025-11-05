from django.core.exceptions import DisallowedHost
from django.urls import reverse
from rest_framework import serializers
from .models import Berita, Komentar


class KomentarSerializer(serializers.ModelSerializer):
    berita = serializers.SlugRelatedField(
        slug_field="judul",
        queryset=Berita.objects.all(),
    )

    class Meta:
        model = Komentar
        fields = ["id", "nama", "tanggal", "isi", "berita"]
        read_only_fields = ["tanggal"]


class BeritaListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Berita
        fields = ["judul", "tanggal", "detail_url"]
        read_only_fields = ["judul", "tanggal", "detail_url"]

    def get_detail_url(self, obj):
        request = self.context.get("request")
        url = reverse("berita-detail", kwargs={"pk": obj.pk})
        if request is not None:
            try:
                return request.build_absolute_uri(url)
            except DisallowedHost:
                pass
        return url


class BeritaDetailSerializer(serializers.ModelSerializer):
    komentar = KomentarSerializer(many=True, read_only=True)

    class Meta:
        model = Berita
        fields = ["id", "judul", "tanggal", "gambar", "isi", "komentar"]
        read_only_fields = ["komentar"]
