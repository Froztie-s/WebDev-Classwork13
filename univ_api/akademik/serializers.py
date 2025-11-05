from rest_framework import serializers
from .models import Prodi, Siswa, Kuliah, Registrasi

class ProdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prodi
        fields = ["nama", "kaprodi"]

class SiswaSerializer(serializers.ModelSerializer):
    prodi = serializers.SlugRelatedField(
        slug_field="nama",
        queryset=Prodi.objects.all(),
    )
    prodi_detail = ProdiSerializer(source="prodi", read_only=True)

    class Meta:
        model = Siswa
        fields = ["id", "nama", "nim", "foto", "prodi", "prodi_detail"]

class KuliahSerializer(serializers.ModelSerializer):
    prodi_detail = ProdiSerializer(source="prodi", read_only=True)

    class Meta:
        model = Kuliah
        fields = ["id", "matkul", "prodi", "prodi_detail", "hari", "sks"]

class RegistrasiSerializer(serializers.ModelSerializer):
    student_detail = SiswaSerializer(source="student", read_only=True)
    kuliah_detail = KuliahSerializer(source="kuliah", read_only=True)

    class Meta:
        model = Registrasi
        fields = ["id", "student", "student_detail", "kuliah", "kuliah_detail"]

    def validate(self, attrs):
        # (Optional rule) Pastikan prodi siswa cocok dengan prodi kuliah
        student = attrs.get("student")
        kuliah = attrs.get("kuliah")
        if student and kuliah and student.prodi_id != kuliah.prodi_id:
            raise serializers.ValidationError("Prodi mahasiswa dan prodi mata kuliah harus sama.")
        return attrs
