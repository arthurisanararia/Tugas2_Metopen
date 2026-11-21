# SCRIPT PRESENTASI + SIMULASI Q&A
### Rancang Bangun Sistem Kalibrasi Otomatis Sensor Tekanan Menggunakan Transduser Referensi Standar
**Kelompok 3 · Instrumentasi Industri & Kalibrasi · 21 November 2026**

| | |
|---|---|
| Total durasi | **10:00 presentasi** + **5:00 tanya jawab** |
| Pembicara A (Nama 1) | Slide 1–5 · Pendahuluan, arsitektur, pneumatik · **3:30** |
| Pembicara B (Nama 2) | Slide 6–8 · Elektronik, akuisisi, kendali · **3:15** |
| Pembicara C (Nama 3) | Slide 9–12 · Hasil kalibrasi, ketidakpastian, penutup · **3:15** |
| Kecepatan bicara acuan | ±140 kata/menit (santai, berhenti di tanda `//`) |
| Total kata naskah | ±1.390 kata ≈ **9,9 menit** @140 kata/menit (target latihan: 9:30) |

> **Cara pakai:** cetak/ buka file ini di HP. Tanda `[SLIDE n]` = ganti slide. Tanda `//` = berhenti 0,5–1 detik (jangan diucapkan). Angka dalam huruf sudah sengaja "dibaca" supaya tidak salah baca saat rekaman.

---

## BAGIAN 1 — SCRIPT PRESENTASI

### PEMBICARA A — Slide 1–5 (0:00 – 3:30)

**[SLIDE 1 · Judul] — 0:00–0:40 (±95 kata)**

Selamat pagi, Bapak/Ibu dosen dan teman-teman. // Kami dari Kelompok 3, dengan topik Instrumentasi Industri dan Kalibrasi. // Judul rancangan kami: Rancang Bangun Sistem Kalibrasi Otomatis Sensor Tekanan Menggunakan Transduser Referensi Standar. // Saya [Nama 1], bersama [Nama 2] dan [Nama 3]. // Dalam sepuluh menit kami menyampaikan latar belakang, rancangan sistem, dan hasil simulasi rancangan. // Target kami sederhana tetapi terukur: rentang nol sampai sepuluh bar, ketidakpastian di bawah nol koma satu persen skala penuh, dan waktu kalibrasi di bawah dua puluh lima menit per sensor.

**[SLIDE 2 · Latar belakang] — 0:40–1:25 (±110 kata)**

Kenapa ini penting? // Kalibrasi tekanan di laboratorium masih manual: operator memutar regulator, menunggu jarum stabil, lalu mencatat. // Untuk satu sensor nol sampai sepuluh bar, cara ini butuh sekitar empat puluh lima menit. // Masalahnya bukan hanya waktu. // Pertama, hasilnya tidak konsisten — pembacaan bergantung pada jam tangan operator dan seberapa cepat katup dibuka, dengan sebaran sampai nol koma tiga persen skala penuh. // Kedua, jejak auditnya lemah: data ditulis tangan, rawan salah catat, dan sulit direkonstruksi. // Dari situ kami rumuskan tiga pertanyaan: bagaimana mengatur tekanan secara otomatis dan presisi, bagaimana mengolah sinyal agar galat di bawah nol koma satu persen, dan berapa ketidakpastian sistemnya.

**[SLIDE 3 · Tujuan & spesifikasi] — 1:25–2:10 (±110 kata)**

Tujuannya empat. // Membangun generator tekanan otomatis nol sampai sepuluh bar. // Mengakuisisi dan mencatat data secara terkomputerisasi. // Menentukan persamaan kalibrasi beserta galat sisa. // Dan menghitung ketidakpastian serta rasio TUR. // Spesifikasi target: resolusi satu milibar, ketidakpastian diperluas maksimum nol koma satu persen skala penuh, repeatability nol koma nol dua persen, dan waktu maksimum dua puluh lima menit untuk enam puluh tiga titik. // Batasannya: fluida kering non-korosif, suhu dua puluh plus minus lima derajat, dan sensor uji piezoresistif nol sampai sepuluh bar. // Kontribusi kami bukan pada komponennya, tetapi pada otomasi yang disertai ketidakpastian terukur — jadi hasil kalibrasi bisa diaudit.

**[SLIDE 4 · Arsitektur] — 2:10–2:55 (±110 kata)**

Ini arsitektur sistemnya. // Ada dua jalur yang bertemu di satu kendali. // Jalur pneumatik: kompresor enam sampai delapan bar, filter-regulator lima mikron, lalu manifold dengan tiga katup solenoid. // Katup kasar Cv nol koma delapan untuk mendekat cepat, katup halus Cv nol koma nol lima untuk presisi, dan katup vent untuk menurunkan tekanan. // Semua bermuara di ruang uji kecil berisi sensor uji dan transduser referensi. // Jalur sinyal: sinyal kedua sensor masuk pengkondisi sinyal, diubah ADC dua puluh empat bit, diolah ESP32, lalu dikirim ke GUI Python. // GUI mengatur setpoint, mikrokontroler menggerakkan katup. // Jadi lingkarannya tertutup: baca tekanan, bandingkan dengan setpoint, koreksi katup.

**[SLIDE 5 · Pneumatik] — 2:55–3:30 (±95 kata)**

Kenapa ruang ujinya kecil, hanya seratus dua puluh mililiter? // Karena volume kecil membuat perubahan tekanan responsif, tetapi masih cukup stabil untuk ditahan. // Di dalamnya sensor uji dan transduser referensi membaca tekanan yang sama — jadi tidak ada koreksi jalur. // Satu hal yang tidak boleh dilewat: uji kebocoran. // Ruang harus turun kurang dari nol koma lima milibar per menit pada sepuluh bar. // Kalau gagal, seluruh data kalibrasi tidak sah, karena penurunan tekanan akan terbaca sebagai perubahan sinyal sensor. // Kami uji sepuluh menit dulu sebelum kalibrasi. // Selanjutnya [Nama 2] menjelaskan sisi elektronik dan kendalinya.

> **Serah terima:** *"Terima kasih [Nama 1]."* → langsung ganti slide, jangan ada jeda kosong.

---

### PEMBICARA B — Slide 6–8 (3:30 – 6:45)

**[SLIDE 6 · Rantai sinyal] — 3:30–4:30 (±140 kata)**

Terima kasih. // Saya lanjut ke rantai sinyal. // Pertanyaan yang sering muncul: apakah ADC dua puluh empat bit berlebihan? // Jawabannya justru sebaliknya. // Dengan rentang sepuluh bar, satu bit setara nol koma enam mikrobar — jauh lebih halus dari kebutuhan kita. // Yang membatasi bukan ADC, tetapi derau di depannya. // Jembatan piezoresistif tiga ratus lima puluh ohm dengan eksitasi lima volt menghasilkan sinyal hanya beberapa milivolt. // Kami pakai INA333 dengan gain seratus, lalu filter RC satu kilo-ohm dan seratus nanofarad dengan cut-off sekitar satu koma enam kilohertz untuk anti-aliasing, ditambah tapis digital dua hertz di firmware. // Hasilnya: derau input satu koma dua mikrovolt rms, ekuivalen sekitar nol koma tiga milibar pada skala tekanan — masih jauh di bawah resolusi sensor uji yang sepuluh milibar. // Artinya akurasi sistem ditentukan transduser referensi yang nol koma nol dua persen, bukan oleh elektroniknya.

**[SLIDE 7 · Prosedur] — 4:30–5:35 (±145 kata)**

Sekarang prosedurnya. // Satu siklus terdiri dari naik, tahan, ukur, turun. // Sistem menyetel setpoint, menunggu sampai stabil, mengambil seribu sampel, lalu pindah ke titik berikutnya. // Kriterianya: error di bawah nol koma nol dua persen skala penuh selama dua detik. // Kalau belum stabil, kendali PI yang mengoreksi — bukan operator yang menunggu. // Totalnya enam puluh tiga titik: sebelas titik tekanan dikali tiga siklus naik-turun, supaya histeresis dan repeatability bisa dihitung dari data yang sama. // Satu titik butuh sekitar dua puluh detik: dua detik tunggu stabil, enam detik akuisisi, sepuluh detik pindah titik. // Enam puluh tiga titik selesai dalam sekitar dua puluh satu menit. // Bandingkan dengan manual yang empat puluh lima menit per sensor. // Dan setiap sampel tersimpan di basis data, jadi bisa direkonstruksi kapan saja.

**[SLIDE 8 · Kendali] — 5:35–6:45 (±150 kata)**

Kendalinya kami pilih PI, bukan PID. // Alasannya: plant tekanan ini orde satu dominan, tidak ada osilasi yang perlu diredam aksi derivatif, dan derivatif justru memperkuat derau pengukuran. // Dengan Kp nol koma lima dan Ti dua koma lima detik, hasil simulasinya begini. // Setpoint enam bar dicapai dengan settling sekitar dua detik pada pita plus minus nol koma dua persen. // Overshoot hanya dua koma lima persen, dan error steady-state nol karena aksi integral. // Perhatikan tiga zona: kuning tunggu stabil, hijau akuisisi seribu sampel, abu-abu pindah titik. // Kenapa overshoot kecil itu penting? // Karena kalau overshoot besar, katup harus vent lalu naik lagi — menambah waktu sekaligus memicu histeresis mekanik. // Pemilihan katup bertingkat juga membantu: kasar untuk mendekat, halus untuk finishing. // Selanjutnya [Nama 3] menyampaikan hasil kalibrasinya.

> **Serah terima:** *"Terima kasih [Nama 2]."* → ganti slide.

---

### PEMBICARA C — Slide 9–12 (6:45 – 10:00)

**[SLIDE 9 · Kurva kalibrasi] — 6:45–7:45 (±135 kata)**

Terima kasih. // Ini hasil kalibrasi dari sebelas titik. // Sumbu horizontal tekanan referensi, sumbu vertikal pembacaan sensor uji. // Garis putus-putus adalah ideal satu banding satu. // Terlihat sensor punya gain sedikit di bawah satu dan offset positif — galat sistematis yang khas. // Sebelum koreksi, galat maksimum nol koma dua dua persen skala penuh. // Setelah koreksi dua titik, span dan offset, turun ke nol koma nol tiga persen. // Persamaannya linear: pembacaan terkoreksi sama dengan a kali pembacaan ditambah b, dengan a dan b dari regresi kuadrat terkecil. // Catatan penting: sisa galat itu bukan sisa acak, melainkan nonlinearitas sensor. // Artinya koreksi dua titik sudah mendekati batasnya; kalau mau lebih kecil lagi, perlu tabel lookup polinomial per segmen.

**[SLIDE 10 · Histeresis & repeatability] — 7:45–8:35 (±105 kata)**

Slide ini memisahkan dua sumber galat yang berbeda. // Kiri: histeresis — selisih pembacaan saat naik dan turun pada tekanan yang sama. // Maksimumnya nol koma nol enam persen skala penuh, sekitar enam milibar, dan terjadi di tengah rentang. // Kanan: repeatability — sebaran pembacaan pada tiga siklus pengulangan, nilainya nol koma nol satu enam persen atau satu koma enam milibar. // Histeresis lebih besar dari repeatability, dan itu wajar: histeresis berasal dari mekanik diafragma dan gesekan seal, sedangkan repeatability lebih didominasi derau elektronik. // Konsekuensinya, prosedur kami selalu tiga siklus penuh, karena kalibrasi satu arah saja akan menyembunyikan histeresis.

**[SLIDE 11 · Anggaran ketidakpastian] — 8:35–9:30 (±125 kata)**

Ini anggaran ketidakpastian, dihitung menurut GUM dengan faktor cakupan k sama dengan dua. // Batang paling panjang bukan dari sistem kami, tetapi dari resolusi sensor uji itu sendiri — sepuluh milibar dibagi akar dua belas. // Kontribusi berikutnya transduser referensi nol koma nol dua persen, lalu histeresis, repeatability, dan drift suhu. // Digabung secara akar jumlah kuadrat, ketidakpastian diperluasnya delapan koma dua milibar, atau nol koma nol delapan dua persen skala penuh. // Rasio TUR terhadap sensor uji kelas nol koma lima persen adalah enam koma satu banding satu. // Syarat minimum ANSI ISA lima satu koma satu adalah empat banding satu. // Jadi sistem ini layak dipakai sebagai kalibrator kerja. // Yang perlu kami akui jujur: kalau sensor uji diganti yang lebih akurat, kontribusi referensi akan dominan — dan itu batas atas rancangan ini.

**[SLIDE 12 · Kesimpulan] — 9:30–10:00 (±90 kata)**

Kesimpulan. // Otomasi enam puluh tiga titik selesai sekitar dua puluh satu menit, dibanding empat puluh lima menit manual per sensor. // Galat sistematis turun dari nol koma dua dua ke nol koma nol tiga persen. // Ketidakpastian nol koma nol delapan dua persen dengan TUR enam koma satu banding satu, dan setiap sampel punya jejak audit digital. // Rencana delapan minggu sudah di minggu kelima: desain selesai, firmware dan fabrikasi berjalan. // Risiko utama kebocoran ruang uji dan drift suhu referensi, keduanya sudah punya mitigasi. // Terima kasih, kami siap menerima pertanyaan.

---

## BAGIAN 2 — SIMULASI Q&A (5:00)

**Aturan main:** masing-masing anggota **menanyakan 1** dan **menjawab 1**. Yang bertanya berdiri/ menatap lawan bicara, bukan membaca slide. Jawaban 40–50 detik, tutup dengan satu kalimat tegas.

### Q1 — [Nama 1] bertanya → [Nama 2] menjawab
**Pertanyaan (10 dtk):**
> "Soal kendali. Kalau katup solenoid punya histeresis mekanik dan deadband, bukankah aksi integral PI bisa tersangkut dan tidak pernah mencapai setpoint? Bagaimana kalian menanganinya?"

**Jawaban [Nama 2] (±45 dtk):**
"Betul, dan itu risiko nyata pada katup solenoida murah. // Ada tiga lapis penanganan. // Pertama, pemilihan katup bertingkat: katup halus punya Cv nol koma nol lima, sehingga satu pulsa duty menghasilkan perubahan tekanan yang lebih kecil dari pita toleransi — jadi sistem tidak pernah "melompati" setpoint. // Kedua, kami beri kompensasi deadband: duty di bawah ambang buka katup tidak dikirim, sehingga integrator tidak menumpuk saat katup sebenarnya tertutup. // Ketiga, aksi integral dibatasi atau di-clamp, supaya tidak terjadi windup saat vent atau saat pindah titik. // Hasil simulasinya error steady-state nol dan tidak ada limit cycle, karena pita histeresis katup lebih kecil dari pita stabil nol koma nol dua persen skala penuh. // Kalau nanti pada fabrikasi ternyata histeresis katup lebih besar, langkah berikutnya adalah gain scheduling per zona tekanan — bukan menambah aksi derivatif."

### Q2 — [Nama 2] bertanya → [Nama 3] menjawab
**Pertanyaan (10 dtk):**
> "Di anggaran ketidakpastian, kontribusi terbesar justru berasal dari sensor uji itu sendiri, bukan dari sistem kalibratornya. Lalu apa artinya angka itu — apakah sistem ini benar-benar akurat, atau kita hanya mengukur keterbatasan sensor yang dikalibrasi?"

**Jawaban [Nama 3] (±50 dtk):**
"Pertanyaan bagus, dan ini perbedaan dua hal yang sering dicampur. // Angka nol koma nol delapan dua persen itu adalah ketidakpastian **hasil kalibrasi** — yaitu ketidakpastian saat kita menyatakan berapa nilai tekanan yang sebenarnya diberikan ke sensor uji. // Karena itu resolusi dan histeresis sensor uji ikut masuk: kita tidak bisa menyatakan hasil lebih baik daripada kemampuan membaca sensor itu. // Kalau yang diminta adalah ketidakpastian **tekanan yang dibangkitkan** oleh kalibrator — tanpa sensor uji — maka komponen DUT dikeluarkan, dan nilainya sekitar nol koma nol tiga persen skala penuh, didominasi transduser referensi. // Jadi sistemnya akurat sebagai pembangkit tekanan; yang membesar adalah ketidakpastian hasil kalibrasi sensor murah. // Dan justru itu gunanya TUR: terhadap sensor kelas nol koma lima persen, rasio enam koma satu banding satu membuktikan sistem ini masih lebih dari empat kali lebih baik dari yang dikalibrasi."

### Q3 — [Nama 3] bertanya → [Nama 1] menjawab
**Pertanyaan (10 dtk):**
> "Volume ruang uji seratus dua puluh mililiter itu angka dari mana? Kalau volume terlalu kecil, bukankah tekanan jadi sangat sensitif terhadap kebocoran dan terhadap pemanasan gas saat kompresi?"

**Jawaban [Nama 1] (±50 dtk):**
"Volume kami pilih dari trade-off tiga hal. // Pertama, kecepatan: konstanta waktu ruang sebanding dengan volume, jadi ruang kecil membuat tekanan naik dalam hitungan detik, bukan puluhan detik. // Kedua, konsumsi udara: ruang kecil hanya butuh sedikit gas per titik, sehingga kompresor tidak bekerja terus-menerus dan suhu suplai lebih stabil. // Ketiga, sensitivitas: benar, volume kecil memperbesar efek kebocoran dan panas kompresi. // Karena itu kami pasang dua syarat desain. // Uji kebocoran wajib: kurang dari nol koma lima milibar per menit pada sepuluh bar — pada seratus dua puluh mililiter itu setara laju kebocoran yang sangat kecil, sehingga ruang harus benar-benar rapat. // Dan untuk panas kompresi, kami tidak menunggu waktu tetap, tetapi menunggu kriteria stabil: error di bawah nol koma nol dua persen selama dua detik. // Jadi efek termal ikut terekam dan baru dianggap selesai setelah reda, bukan diasumsikan."

**Penutup [Nama 1] (10 dtk):**
"Demikian presentasi Kelompok 3. Terima kasih atas perhatian Bapak/Ibu, kami siap menerima pertanyaan lanjutan."

> Total Q&A ±4:00–4:30 → masih ada sisa waktu untuk 1 pertanyaan tak terduga dari dosen (pakai bank di bawah).

---

## BAGIAN 3 — BANK JAWABAN CEPAT (kalau dosen ikut bertanya)

| Pertanyaan dosen | Jawaban inti (30 dtk) |
|---|---|
| Kenapa tidak pakai dead-weight tester? | Dead-weight sangat akurat tetapi statis, manual, dan tidak bisa menguji sensor terpasang/ dinamis. Kami butuh pembangkit tekanan yang otomatis dan terekam. |
| Bagaimana traceability ke SI? | Transduser referensi dikalibrasi ke laboratorium terakreditasi (KAN) yang tertelusur ke standar primer; sertifikatnya jadi dasar rantai ketertelusuran. |
| Kenapa 11 titik, bukan 5 atau 21? | Titik tiap 10 % FS: 0, 10, 20, … 100 % → 11 titik. Cukup untuk melihat nonlinearitas dan histeresis, tanpa menambah waktu berlebihan. |
| Kenapa k = 2? | Tingkat kepercayaan ±95 %, konvensi GUM dan praktik kalibrasi internasional. |
| Apa efek suhu 20 ± 5 °C? | Drift sensor piezoresistif tipikal 0,02 % FS/°C, jadi ±5 °C bisa berarti 0,1 % FS. Karena itu suhu ruang dijaga dan dicatat; setelah kompensasi, residu yang masuk anggaran hanya 1 mbar (0,01 % FS). |
| Kenapa ESP32, bukan PLC atau PC? | ESP32 cukup untuk PI 10 Hz dan ADC SPI, berbiaya rendah, dan punya Wi-Fi untuk basis data. PLC lebih mahal dan tidak perlu untuk satu loop. |
| Apa kebaruannya? Ini kan cuma otomasi? | Kebaruan pada integrasi: otomasi titik ukur + uji kebocoran otomatis + anggaran ketidakpastian dan TUR yang dilaporkan per sensor, bukan hanya "alatnya jalan". |
| Bagaimana kalau transduser referensi rusak/ drift? | Ada kalibrasi silang harian dengan indikator tekanan sekunder dan pencatatan suhu; hasil di luar batas ditolak oleh perangkat lunak, bukan diterima diam-diam. |

---

## BAGIAN 4 — CEK KONSISTENSI SLIDE (status: sudah diperbaiki di skrip)

Saya sudah menyamakan angka yang tadinya tidak konsisten. Kalau kamu **menyusun slide sendiri**, pakai daftar ini sebagai acuan supaya tidak balik ke angka lama.

1. **"45 menit" harus per sensor, bukan per titik.** Slide 12 tadinya menulis *"vs ± 45 menit manual per titik"*, padahal slide 2 menyebut 45 menit untuk satu sensor (11 titik). Sudah saya ubah jadi **"vs ± 45 menit manual per sensor"**.
2. **TUR: sekarang 6,1 : 1** (tadinya 5,6 : 1, tidak cocok dengan U = 8,2 mbar). Hitungannya 0,5 % FS ÷ 0,082 % FS = 6,1. Angka 5,6 hanya benar kalau U = 8,9 mbar. Saya pilih memperbaiki TUR karena U sudah dipakai di tiga slide lain. Sudah diubah di `assets/figures.py` (caption kini dihitung otomatis), `build_pptx.py` (slide 3 dan 11), dan di script.
3. **Nama masih placeholder.** Ganti `[Nama 1] · [Nama 2] · [Nama 3]` di slide 1 dan slide 12, juga di script (jangan sampai terbaca "nama satu").
4. **Filter RC sekarang jelas.** Diagram blok tadinya menulis *"filter RC 2 Hz"* sementara skematik menulis *"1,6 kHz"*. Sudah jadi **"RC 1,6 kHz + LPF 2 Hz"** — 1,6 kHz anti-aliasing analog, 2 Hz tapis digital di firmware.
5. **Gambar di `assets/png/` sudah versi terbaru** (diagram blok & grafik ketidakpastian diregenerasi). File `.pptx` lama masih memuat versi sebelum perbaikan, jadi kalau kamu memakai pptx itu, ganti dua gambar tersebut — atau sisipkan ulang PNG dari `assets/png/`.
6. **Cek durasi baca.** Naskah ±1.390 kata. Kalau latihan lewat 10:00, potong yang paling aman: satu kalimat di slide 2 dan satu kalimat di slide 10 (alur tidak berubah).

---

## BAGIAN 5 — CHECKLIST SEBELUM UPLOAD (target 12:00)

- [ ] Ganti semua `[Nama 1/2/3]` di slide **dan** di script (baca ulang, jangan sampai terbaca "nama satu").
- [ ] Rekam dengan **share screen slide** + wajah kecil di pojok (opsional). Resolusi 1080p, audio dari mic eksternal/ headset.
- [ ] Latihan 1× dengan stopwatch; target 9:30 supaya ada ruang napas.
- [ ] Rekam Q&A sebagai bagian video yang sama (satu take, jangan dipotong — kesan "live").
- [ ] Upload YouTube, judul: `Tugas Besar Metopen — Sistem Kalibrasi Otomatis Sensor Tekanan (Kelompok 3)`, deskripsi berisi nama anggota + daftar isi waktu (timestamp per pembicara).
- [ ] Set **Unlisted** kalau tidak mau publik, lalu share link ke WAG sebelum **14:00 WIB**.
- [ ] Cek link di mode incognito/ HP sebelum kirim.

---

## BAGIAN 6 — PETA ASET KE SLIDE (untuk menyusun PPT sendiri)

Semua gambar ada di `assets/png/`, rasio 16:9 sudah pas untuk slide. Kalau butuh mengubah angka di gambar, edit `assets/figures.py` lalu jalankan `python assets/figures.py`.

| Slide | Isi | File aset |
|---|---|---|
| 1 | Judul | *(tanpa gambar — cukup teks + blok warna)* |
| 2 | Latar belakang, 3 kartu masalah | *(tanpa gambar)* |
| 3 | Tujuan, spesifikasi, 3 angka kunci | *(tanpa gambar)* |
| 4 | Arsitektur sistem | `01_diagram_blok.png` |
| 5 | Skematik pneumatik (P&ID) | `02_skematik_pneumatik.png` |
| 6 | Rantai sinyal (jembatan → INA333 → ADC → ESP32) | `03_rantai_sinyal.png` |
| 7 | Flowchart perangkat lunak | `07_flowchart.png` |
| 8 | Respons kendali PI (grafik step response) | `08_respons_kendali.png` |
| 9 | Kurva kalibrasi + galat sebelum/ sesudah | `04_kurva_kalibrasi.png` |
| 10 | Histeresis & repeatability | `05_histeresis_repeatability.png` |
| 11 | Anggaran ketidakpastian (bar + donat) | `06_ketidakpastian.png` |
| 12 | Kesimpulan + jadwal 8 minggu | `09_gantt.png` |

**Angka yang harus sama di semua slide** (kalau kamu mengetik ulang, jangan diubah):

- Rentang 0–10 bar · resolusi 1 mbar · target U ≤ 0,1 % FS
- 11 titik × 3 siklus = **63 titik**, ≈ **21 menit** per sensor (manual ± 45 menit)
- Settling ≈ **2,0 s**, overshoot **2,5 %**, error steady-state **0**
- Galat **0,22 % → 0,03 % FS**; histeresis **0,06 % FS**; repeatability **0,016 % FS**
- **U = 8,2 mbar = 0,082 % FS** (k = 2) → **TUR 6,1 : 1** vs DUT kelas 0,5 % FS
