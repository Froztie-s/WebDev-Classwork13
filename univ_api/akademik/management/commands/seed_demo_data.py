from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from akademik.models import Kuliah, Prodi, Registrasi, Siswa
from berita.models import Berita, Komentar


class Command(BaseCommand):
    help = "Seed predictable demo data for the akademik app so features can be tested quickly."

    def handle(self, *args, **options):
        self.stdout.write("Seeding akademik & berita demo data...")
        with transaction.atomic():
            prodi_map = self._seed_prodi()
            siswa_map = self._seed_siswa(prodi_map)
            kuliah_map = self._seed_kuliah(prodi_map)
            self._seed_registrasi(siswa_map, kuliah_map)
            berita_map = self._seed_berita()
            self._seed_komentar(berita_map)
        self.stdout.write(self.style.SUCCESS("Demo data ready."))

    def _seed_prodi(self):
        data = [
            ("if", {"nama": "Teknik Informatika", "kaprodi": "Dr. Budi Santoso"}),
            ("si", {"nama": "Sistem Informasi", "kaprodi": "Dr. Ratna Dewi"}),
            ("ti", {"nama": "Teknik Industri", "kaprodi": "Dr. Andi Wirawan"}),
        ]
        result = {}
        for key, payload in data:
            obj, created = Prodi.objects.get_or_create(
                nama=payload["nama"], defaults={"kaprodi": payload["kaprodi"]}
            )
            if not created and obj.kaprodi != payload["kaprodi"]:
                obj.kaprodi = payload["kaprodi"]
                obj.save(update_fields=["kaprodi"])
            result[key] = obj
        return result

    def _seed_siswa(self, prodi_map):
        data = [
            ("2101001", {"nama": "Andi Pratama", "prodi": "if"}),
            ("2101002", {"nama": "Siti Lestari", "prodi": "if"}),
            ("2102001", {"nama": "Rudi Hartono", "prodi": "si"}),
            ("2102002", {"nama": "Nina Kartika", "prodi": "si"}),
            ("2103001", {"nama": "Wawan Kurniawan", "prodi": "ti"}),
        ]
        result = {}
        for nim, payload in data:
            defaults = {
                "nama": payload["nama"],
                "prodi": prodi_map[payload["prodi"]],
            }
            obj, created = Siswa.objects.get_or_create(nim=nim, defaults=defaults)
            if not created:
                changed = False
                if obj.nama != payload["nama"]:
                    obj.nama = payload["nama"]
                    changed = True
                if obj.prodi != defaults["prodi"]:
                    obj.prodi = defaults["prodi"]
                    changed = True
                if changed:
                    obj.save(update_fields=["nama", "prodi"])
            result[nim] = obj
        return result

    def _seed_kuliah(self, prodi_map):
        data = [
            ("if_algo", {"matkul": "Algoritma dan Struktur Data", "prodi": "if", "hari": "Senin", "sks": 3}),
            ("if_pbo", {"matkul": "Pemrograman Berorientasi Objek", "prodi": "if", "hari": "Rabu", "sks": 3}),
            ("si_akuntansi", {"matkul": "Sistem Informasi Akuntansi", "prodi": "si", "hari": "Selasa", "sks": 3}),
            ("si_erp", {"matkul": "Pengantar ERP", "prodi": "si", "hari": "Kamis", "sks": 2}),
            ("ti_ops", {"matkul": "Manajemen Operasi", "prodi": "ti", "hari": "Senin", "sks": 2}),
            ("ti_qc", {"matkul": "Quality Control", "prodi": "ti", "hari": "Jumat", "sks": 2}),
        ]

        result = {}
        for key, payload in data:
            defaults = {
                "prodi": prodi_map[payload["prodi"]],
                "hari": payload["hari"],
                "sks": payload["sks"],
            }
            obj, created = Kuliah.objects.get_or_create(
                matkul=payload["matkul"],
                prodi=defaults["prodi"],
                hari=defaults["hari"],
                defaults={"sks": defaults["sks"]},
            )
            if not created and obj.sks != defaults["sks"]:
                obj.sks = defaults["sks"]
                obj.save(update_fields=["sks"])
            result[key] = obj
        return result

    def _seed_registrasi(self, siswa_map, kuliah_map):
        data = [
            ("2101001", "if_algo"),
            ("2101001", "if_pbo"),
            ("2101002", "if_algo"),
            ("2102001", "si_akuntansi"),
            ("2102002", "si_erp"),
            ("2103001", "ti_ops"),
            ("2103001", "ti_qc"),
        ]
        for nim, kuliah_key in data:
            Registrasi.objects.get_or_create(
                student=siswa_map[nim],
                kuliah=kuliah_map[kuliah_key],
            )

    def _seed_berita(self):
        data = [
            (
                "kampus_merdeka",
                {
                    "judul": "Kampus Merdeka Hadirkan Kuliah Industri",
                    "tanggal": date(2025, 5, 10),
                    "isi": (
                        "Universitas Nusantara kembali menggelar program Kuliah Industri bersama mitra "
                        "strategis dari sektor teknologi. Mahasiswa mendapat kesempatan magang singkat "
                        "dan mengikuti workshop mengenai tren kecerdasan buatan."
                    ),
                },
            ),
            (
                "festival_budaya",
                {
                    "judul": "Festival Budaya Nusantara Ramaikan Kampus",
                    "tanggal": date(2025, 5, 18),
                    "isi": (
                        "Unit Kegiatan Mahasiswa Seni mempersembahkan Festival Budaya Nusantara dengan "
                        "menampilkan tarian daerah, pameran kuliner, serta lokakarya batik. "
                        "Acara ini terbuka bagi mahasiswa dan masyarakat umum."
                    ),
                },
            ),
            (
                "beasiswa_unggulan",
                {
                    "judul": "Beasiswa Unggulan 2025 Resmi Dibuka",
                    "tanggal": date(2025, 5, 22),
                    "isi": (
                        "Biro Kemahasiswaan mengumumkan pembukaan Beasiswa Unggulan 2025 untuk mahasiswa "
                        "berprestasi akademik dan aktif berorganisasi. Pendaftaran dilakukan melalui "
                        "portal resmi sampai akhir Juni."
                    ),
                },
            ),
        ]

        result = {}
        for key, payload in data:
            obj, created = Berita.objects.get_or_create(
                judul=payload["judul"],
                defaults={
                    "tanggal": payload["tanggal"],
                    "isi": payload["isi"],
                },
            )
            if not created:
                changed_fields = []
                if obj.tanggal != payload["tanggal"]:
                    obj.tanggal = payload["tanggal"]
                    changed_fields.append("tanggal")
                if obj.isi != payload["isi"]:
                    obj.isi = payload["isi"]
                    changed_fields.append("isi")
                if changed_fields:
                    obj.save(update_fields=changed_fields)
            result[key] = obj
        return result

    def _seed_komentar(self, berita_map):
        data = [
            ("kampus_merdeka", {"nama": "Dewi Larasati", "isi": "Program ini membantu kami memahami kebutuhan industri."}),
            ("kampus_merdeka", {"nama": "Rizky Saputra", "isi": "Semoga kesempatan magang diperluas ke jurusan lain."}),
            ("festival_budaya", {"nama": "Nadia Fitri", "isi": "Tidak sabar melihat penampilan tari tradisionalnya!"}),
            ("beasiswa_unggulan", {"nama": "Fajar Hidayat", "isi": "Terima kasih atas informasinya, saya akan mendaftar."}),
        ]
        for berita_key, payload in data:
            Komentar.objects.get_or_create(
                berita=berita_map[berita_key],
                nama=payload["nama"],
                isi=payload["isi"],
            )
