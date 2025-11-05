from django.db import models

# Create your models here.
class Prodi(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    kaprodi = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

def siswa_photo_path(instance, filename):
    return f'siswa_photos/{instance.nim}/{filename}'

class Siswa(models.Model):
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=20, unique=True)
    foto = models.ImageField(upload_to=siswa_photo_path, blank=True, null=True) # type: ignore
    prodi = models.ForeignKey(Prodi, on_delete=models.PROTECT, related_name='siswa')

    def __str__(self):
        return f"{self.nim} ({self.nama})"
    

Hari_Choices = [
    ('Senin', 'Senin'),
    ('Selasa', 'Selasa'),
    ('Rabu', 'Rabu'),
    ('Kamis', 'Kamis'),
    ('Jumat', 'Jumat'),
    ('Sabtu', 'Sabtu'),
    ('Minggu', 'Minggu'),
]

class Kuliah(models.Model):
    matkul = models.CharField(max_length=100)
    prodi = models.ForeignKey(Prodi, on_delete=models.PROTECT, related_name='kuliah')
    hari = models.CharField(max_length=10, choices=Hari_Choices)
    sks = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('matkul', 'prodi', 'hari')

    def __str__(self):
        return f"{self.matkul} - {self.prodi.nama} ({self.hari})"
    
class Registrasi(models.Model):
    student = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name="registrasi")
    kuliah = models.ForeignKey(Kuliah, on_delete=models.CASCADE, related_name="registrasi")

    class Meta:
        unique_together = ("student", "kuliah")  # no duplicate enrollments

    def __str__(self):
        return f"{self.student.nim} -> {self.kuliah.matkul}"