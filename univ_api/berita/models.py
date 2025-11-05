from django.db import models


def berita_image_path(instance, filename):
    """Store berita images under berita/<slug>/filename."""
    return f"berita/{instance.id or 'new'}/{filename}"


class Berita(models.Model):
    judul = models.CharField(max_length=200, unique=True)
    tanggal = models.DateField()
    gambar = models.ImageField(upload_to=berita_image_path, blank=True, null=True)
    isi = models.TextField()

    class Meta:
        ordering = ["-tanggal"]

    def __str__(self):
        return self.judul


class Komentar(models.Model):
    berita = models.ForeignKey(Berita, related_name="komentar", on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    tanggal = models.DateTimeField(auto_now_add=True)
    isi = models.TextField()

    class Meta:
        ordering = ["-tanggal"]

    def __str__(self):
        return f"{self.nama} on {self.berita.judul}"
