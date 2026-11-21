# -*- coding: utf-8 -*-
"""
Membangun deck presentasi (16:9, 12 slide) dari aset di assets/png.
Output: Presentasi_Kalibrasi_Otomatis_Sensor_Tekanan.pptx
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(HERE, "assets", "png")
# PPTX_OUT boleh diisi lewat environment variable supaya bisa membuat file
# sementara (misal untuk render preview) tanpa menimpa deck utama.
OUT = os.environ.get("PPTX_OUT") or os.path.join(
    HERE, "Presentasi_Kalibrasi_Otomatis_Sensor_Tekanan.pptx")

NAVY = RGBColor(0x0F, 0x2A, 0x44)
NAVY2 = RGBColor(0x1B, 0x3F, 0x63)
TEAL = RGBColor(0x0E, 0x9F, 0x8E)
TEAL_L = RGBColor(0xD7, 0xF0, 0xEC)
AMBER = RGBColor(0xE3, 0x9A, 0x28)
RED = RGBColor(0xC9, 0x46, 0x3D)
GRAY = RGBColor(0x6B, 0x7A, 0x8A)
LGRAY = RGBColor(0xE8, 0xED, 0xF2)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CREAM = RGBColor(0xFA, 0xF7, 0xF2)

FONT = "Segoe UI"
FONT_B = "Segoe UI Semibold"

W, H = 13.333, 7.5

prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(H)
BLANK = prs.slide_layouts[6]

GROUP = "Kelompok 3  ·  Instrumentasi Industri & Kalibrasi"
FOOT = "Rancang Bangun Sistem Kalibrasi Otomatis Sensor Tekanan"


# ------------------------------------------------------------------ helpers
def tb(slide, x, y, w, h, text, size=14, color=NAVY, bold=False, font=FONT,
       align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.0, italic=False,
       space_after=0):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(space_after)
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.name = font
        r.font.color.rgb = color
    return box


def rect(slide, x, y, w, h, fill=None, line=None, lw=1.0, shape=MSO_SHAPE.RECTANGLE,
         radius=None, shadow=False):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(lw)
    s.shadow.inherit = shadow
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    s.text_frame.word_wrap = True
    return s


def chip(slide, x, y, w, h, text, fill, color, size=10.5, bold=True):
    s = rect(slide, x, y, w, h, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    tf = s.text_frame
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = FONT_B
    r.font.color.rgb = color
    return s


def base(slide, kicker, title, lead=None, dark=False):
    # panel putih
    bg = NAVY if dark else WHITE
    rect(slide, 0, 0, W, H, fill=bg)
    # aksen kiri
    rect(slide, 0, 0, 0.085, H, fill=TEAL if not dark else AMBER)
    kc = AMBER if dark else TEAL
    tc = WHITE if dark else NAVY
    lc = RGBColor(0xB8, 0xC7, 0xD6) if dark else GRAY
    tb(slide, 0.62, 0.40, 11.9, 0.26, kicker.upper(), 10, kc, True, FONT_B)
    tb(slide, 0.60, 0.68, 12.1, 0.62, title, 25, tc, True, FONT_B)
    if lead:
        tb(slide, 0.62, 1.36, 11.6, 0.34, lead, 12.5, lc, False, FONT, italic=False)


def footer(slide, n):
    rect(slide, 0.62, 7.00, 12.12, 0.008, fill=LGRAY)
    tb(slide, 0.62, 7.10, 7.2, 0.24, GROUP, 8.5, GRAY)
    tb(slide, 10.2, 7.10, 2.55, 0.24, f"{FOOT}  |  {n}", 8.5, GRAY,
       align=PP_ALIGN.RIGHT)


def picture(slide, name, top, max_w=11.9, max_h=4.85, left=None):
    p = os.path.join(PNG, name)
    iw, ih = Image.open(p).size
    ar = iw / ih
    w = max_w
    h = w / ar
    if h > max_h:
        h = max_h
        w = h * ar
    x = (W - w) / 2 if left is None else left
    slide.shapes.add_picture(p, Inches(x), Inches(top), Inches(w), Inches(h))
    return x, top, w, h


def bullets(slide, x, y, w, items, size=13, gap=0.42, color=NAVY, bullet_color=TEAL,
            sub_size=10.5):
    """items: list of (text, sub) atau str"""
    cy = y
    for it in items:
        main, sub = (it, None) if isinstance(it, str) else it
        rect(slide, x, cy + 0.075, 0.085, 0.085, fill=bullet_color,
             shape=MSO_SHAPE.OVAL)
        tb(slide, x + 0.26, cy, w - 0.26, 0.30, main, size, color, True, FONT_B)
        if sub:
            tb(slide, x + 0.26, cy + 0.29, w - 0.26, 0.30, sub, sub_size, GRAY)
            cy += gap + 0.16
        else:
            cy += gap
    return cy


def metric(slide, x, y, w, h, value, label, accent=TEAL):
    rect(slide, x, y, w, h, fill=CREAM, line=LGRAY, lw=0.75)
    rect(slide, x, y, 0.05, h, fill=accent)
    tb(slide, x + 0.26, y + 0.20, w - 0.45, 0.52, value, 24, accent, True, FONT_B)
    tb(slide, x + 0.26, y + 0.78, w - 0.42, 0.60, label, 10, GRAY, False, FONT,
       spacing=1.1)


def note(slide, x, y, w, text, accent=AMBER, size=10.5):
    rect(slide, x, y, w, 0.52, fill=RGBColor(0xFD, 0xF4, 0xE3), line=None)
    rect(slide, x, y, 0.045, 0.52, fill=accent)
    tb(slide, x + 0.20, y + 0.12, w - 0.32, 0.34, text, size, NAVY2, False, FONT)


# ================================================================== 1. JUDUL
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, fill=NAVY)
rect(s, 0, 0, 0.10, H, fill=AMBER)
# blok dekoratif kanan
rect(s, 9.05, 0, 4.28, H, fill=NAVY2)
rect(s, 9.05, 0, 0.02, H, fill=TEAL)

tb(s, 0.85, 0.78, 8.0, 0.30, "TUGAS BESAR METODOLOGI PENELITIAN", 11,
   AMBER, True, FONT_B)
tb(s, 0.85, 1.22, 8.0, 0.32, "Seminar Rancangan Tugas Akhir  ·  21 November 2026", 11,
   RGBColor(0xB8, 0xC7, 0xD6), False, FONT)

tb(s, 0.85, 1.95, 7.9, 2.55,
   "Rancang Bangun Sistem\nKalibrasi Otomatis Sensor\nTekanan Menggunakan\nTransduser Referensi Standar",
   33, WHITE, True, FONT_B, spacing=1.12)

rect(s, 0.88, 4.72, 1.35, 0.05, fill=TEAL)
tb(s, 0.85, 4.95, 7.9, 0.62,
   "Topik: Instrumentasi Industri & Kalibrasi", 13.5, TEAL, True, FONT_B)
tb(s, 0.85, 5.38, 7.9, 0.70,
   "Otomasi titik ukur · kompensasi galat · anggaran ketidakpastian  |  target CMC ≤ 0,1 % FS",
   11.5, RGBColor(0xB8, 0xC7, 0xD6), False, FONT, spacing=1.25)

tb(s, 0.85, 6.35, 7.9, 0.30, "Kelompok 3  ·  3 anggota", 10.5, AMBER, True, FONT_B)
tb(s, 0.85, 6.65, 7.9, 0.55,
   "[Nama 1]  ·  [Nama 2]  ·  [Nama 3]", 12, WHITE, False, FONT)

# panel kanan: ringkasan angka
tb(s, 9.55, 0.95, 3.3, 0.28, "SASARAN RANCANGAN", 9.5, AMBER, True, FONT_B)
for i, (v, l) in enumerate([("0–10 bar", "rentang ukur"),
                            ("0,02 % FS", "akurasi transduser referensi"),
                            ("63 titik", "11 titik × 3 siklus, otomatis"),
                            ("≈ 21 menit", "waktu kalibrasi per sensor")]):
    y = 1.45 + i * 1.30
    tb(s, 9.55, y, 3.3, 0.42, v, 19, WHITE, True, FONT_B)
    tb(s, 9.55, y + 0.44, 3.3, 0.44, l, 9.8, RGBColor(0xA9, 0xBC, 0xCE), False, FONT,
       spacing=1.1)

# ================================================================== 2. LATAR BELAKANG
s = prs.slides.add_slide(BLANK)
base(s, "01  ·  Pendahuluan", "Kenapa kalibrasi tekanan masih manual?",
     "Kalibrasi manual akurat, tetapi lambat, subjektif, dan sulit diaudit.")

# tiga kartu masalah
cards = [
    ("Lambat & mahal", "Satu sensor 0–10 bar butuh ±45 menit\nbila dikerjakan manual.", "45 mnt"),
    ("Tidak konsisten", "Pembacaan bergantung pada jam tangan\noperator dan kecepatan membuka katup.", "± 0,3 % FS"),
    ("Jejak audit lemah", "Data ditulis tangan, rawan salah catat,\ndan sulit direkonstruksi saat audit.", "manual"),
]
for i, (t, d, tag) in enumerate(cards):
    x = 0.62 + i * 4.12
    rect(s, x, 1.92, 3.86, 2.10, fill=CREAM, line=LGRAY, lw=0.75)
    rect(s, x, 1.92, 3.86, 0.055, fill=RED)
    tb(s, x + 0.30, 2.12, 3.26, 0.30, tag.upper(), 9.5, RED, True, FONT_B)
    tb(s, x + 0.30, 2.46, 3.26, 0.34, t, 14.5, NAVY, True, FONT_B)
    tb(s, x + 0.30, 2.86, 3.28, 0.90, d, 10.5, GRAY, False, FONT, spacing=1.30)

# rumusan masalah + tujuan
rect(s, 0.62, 4.32, 6.55, 2.42, fill=WHITE, line=LGRAY, lw=0.75)
tb(s, 0.90, 4.50, 6.0, 0.26, "RUMUSAN MASALAH", 9.5, TEAL, True, FONT_B)
bullets(s, 0.90, 4.86, 6.05, [
    ("Bagaimana mengatur tekanan otomatis dan presisi 0–10 bar?", None),
    ("Bagaimana mengolah sinyal sensor agar galat < 0,1 % FS?", None),
    ("Berapa ketidakpastian sistem dan apakah layak sebagai standar kerja?", None),
], size=11.5, gap=0.44, sub_size=9.5)

rect(s, 7.42, 4.32, 5.30, 2.42, fill=NAVY, line=None)
tb(s, 7.70, 4.50, 4.8, 0.26, "PEMBAGIAN PERAN  ·  10 MENIT", 9.5, AMBER, True, FONT_B)
roles = [("[Nama 1]", "Pendahuluan, arsitektur, pneumatik", "3:30"),
         ("[Nama 2]", "Elektronik, akuisisi, kendali", "3:15"),
         ("[Nama 3]", "Hasil kalibrasi, ketidakpastian", "3:15")]
for i, (nm, task, t) in enumerate(roles):
    y = 4.88 + i * 0.62
    tb(s, 7.70, y, 1.35, 0.28, nm, 11, WHITE, True, FONT_B)
    tb(s, 9.02, y, 2.75, 0.28, task, 9.8, RGBColor(0xB8, 0xC7, 0xD6), False, FONT)
    tb(s, 11.86, y, 0.62, 0.28, t, 9.8, AMBER, True, FONT_B, align=PP_ALIGN.RIGHT)

footer(s, 2)

# ================================================================== 3. TUJUAN & SPESIFIKASI
s = prs.slides.add_slide(BLANK)
base(s, "02  ·  Tujuan & Batasan", "Apa yang akan dibangun dan sejauh mana akurasinya",
     "Sistem kalibrasi otomatis berbasis ruang uji bertekanan dengan transduser referensi kelas 0,02 % FS.")

tb(s, 0.62, 1.90, 5.55, 0.28, "TUJUAN", 9.8, TEAL, True, FONT_B)
bullets(s, 0.62, 2.24, 5.60, [
    ("Membangun generator tekanan otomatis 0–10 bar", "katup solenoid + kendali PI"),
    ("Akuisisi & pencatatan data terkomputerisasi", "ADC 24-bit, GUI, basis data"),
    ("Menentukan persamaan kalibrasi dan galat sisa", "regresi linear, histeresis"),
    ("Menghitung ketidakpastian dan rasio TUR", "GUM, k = 2"),
], size=12.5, gap=0.40, sub_size=10)

tb(s, 6.55, 1.90, 6.2, 0.28, "SPESIFIKASI TARGET", 9.8, AMBER, True, FONT_B)
rows = [("Rentang ukur", "0 – 10 bar (gauge)"),
        ("Resolusi tampilan", "1 mbar"),
        ("Akurasi sistem (U, k=2)", "≤ 0,1 % FS  (≤ 10 mbar)"),
        ("Repeatability", "≤ 0,02 % FS"),
        ("Waktu per sensor", "≤ 25 menit untuk 63 titik"),
        ("Antarmuka", "GUI Python + ekspor laporan PDF")]
for i, (k, v) in enumerate(rows):
    y = 2.24 + i * 0.50
    rect(s, 6.55, y, 6.18, 0.44, fill=CREAM if i % 2 == 0 else WHITE, line=None)
    tb(s, 6.78, y + 0.10, 2.35, 0.26, k, 10.5, GRAY, False, FONT)
    tb(s, 9.20, y + 0.09, 3.40, 0.28, v, 10.8, NAVY, True, FONT_B)

note(s, 6.55, 5.34, 6.18,
     "Batasan: fluida kering non-korosif, suhu 20 ± 5 °C, DUT piezoresistif 0–10 bar.")

rect(s, 6.55, 6.06, 6.18, 0.80, fill=NAVY, line=None)
tb(s, 6.80, 6.18, 5.7, 0.26, "KONTRIBUSI TERHADAP KEBARUAN", 9.2, AMBER, True, FONT_B)
tb(s, 6.80, 6.46, 5.7, 0.30,
   "Otomasi + ketidakpastian terukur → kalibrasi dapat diaudit, bukan sekadar “percaya pada alat”.", 9.4, WHITE,
   False, FONT)

metric(s, 0.62, 4.86, 1.86, 1.30, "6,1 : 1", "TUR terhadap DUT kelas 0,5 % FS", TEAL)
metric(s, 2.62, 4.86, 1.86, 1.30, "0,082 %", "ketidakpastian diperluas (FS)", TEAL)
metric(s, 4.62, 4.86, 1.96, 1.30, "63", "titik ukur otomatis per sensor", AMBER)

footer(s, 3)

# ================================================================== 4. ARSITEKTUR
s = prs.slides.add_slide(BLANK)
base(s, "03  ·  Rancangan Sistem", "Arsitektur: dua jalur, satu kendali",
     "Jalur pneumatik membangkitkan tekanan; jalur sinyal membaca, menghitung, dan mengaktuasi katup.")
picture(s, "01_diagram_blok.png", 1.80, max_w=12.15, max_h=4.90)
note(s, 0.62, 6.42, 12.12,
     "Kunci desain: katup kasar (Cv 0,8) untuk mendekat cepat, katup halus (Cv 0,05) untuk presisi, katup vent untuk menurunkan tekanan.")
footer(s, 4)

# ================================================================== 5. PNEUMATIK
s = prs.slides.add_slide(BLANK)
base(s, "04  ·  Perancangan Pneumatik", "Skematik: ruang uji kecil, tiga katup, satu referensi",
     "Volume ruang uji 120 mL membuat perubahan tekanan responsif namun tetap stabil.")
picture(s, "02_skematik_pneumatik.png", 1.78, max_w=11.55, max_h=4.55)
note(s, 0.62, 6.40, 12.12,
     "Uji kebocoran wajib: penurunan < 0,5 mbar/menit pada 10 bar — jika gagal, seluruh data kalibrasi tidak sah.")
footer(s, 5)

# ================================================================== 6. ELEKTRONIK
s = prs.slides.add_slide(BLANK)
base(s, "05  ·  Akuisisi Sinyal", "Rantai sinyal: resolusi bukan bottleneck",
     "ADC 24-bit memberi resolusi 0,6 µbar, jauh di bawah resolusi DUT — akurasi ditentukan referensi.")
picture(s, "03_rantai_sinyal.png", 1.72, max_w=12.05, max_h=3.78)
# tiga angka kunci
for i, (v, l, c) in enumerate([
        ("1,2 µV rms", "derau input pengkondisi sinyal", TEAL),
        ("≈ 0,3 mbar", "ekuivalen derau pada skala tekanan", TEAL),
        ("0,02 % FS", "akurasi transduser referensi (2 mbar)", AMBER)]):
    metric(s, 0.62 + i * 4.12, 5.66, 3.86, 1.16, v, l, c)

footer(s, 6)

# ================================================================== 7. PROSEDUR
s = prs.slides.add_slide(BLANK)
base(s, "06  ·  Metode & Perangkat Lunak", "Satu siklus = naik, tahan, ukur, turun",
     "Setiap titik ditahan sampai stabil, lalu 1.000 sampel dirata-rata untuk menekan derau acak.")
picture(s, "07_flowchart.png", 1.74, max_w=11.75, max_h=4.30)
note(s, 0.62, 6.20, 12.12,
     "Kriteria stabil: |e| < 0,02 % FS selama 2 detik. Bila belum stabil, PI mengoreksi duty katup halus — bukan menunggu operator.")
footer(s, 7)

# ================================================================== 8. KENDALI
s = prs.slides.add_slide(BLANK)
base(s, "07  ·  Kendali Tekanan", "Respons kendali: cepat, overshoot kecil, tanpa offset",
     "PI 10 Hz dengan pemilihan katup bertingkat; error steady-state nol karena aksi integral.")
picture(s, "08_respons_kendali.png", 1.78, max_w=11.95, max_h=4.05)
for i, (v, l, c) in enumerate([
        ("2,0 s", "waktu settling (pita ±0,2 % FS)", TEAL),
        ("2,5 %", "overshoot terhadap setpoint 6 bar", AMBER),
        ("0", "error steady-state (aksi integral)", TEAL)]):
    metric(s, 0.62 + i * 4.12, 5.72, 3.86, 1.08, v, l, c)
footer(s, 8)

# ================================================================== 9. HASIL KALIBRASI
s = prs.slides.add_slide(BLANK)
base(s, "08  ·  Hasil", "Kurva kalibrasi: galat 0,22 % FS turun ke 0,03 % FS",
     "Koreksi dua titik (span & offset) menghapus sebagian besar galat sistematis sensor.")
picture(s, "04_kurva_kalibrasi.png", 1.76, max_w=12.20, max_h=4.15)
note(s, 0.62, 6.10, 12.12,
     "Sisa galat 0,03 % FS berasal dari nonlinearitas sensor — tidak bisa dihilangkan dengan koreksi dua titik, perlu tabel lookup polinomial.")
footer(s, 9)

# ================================================================== 10. HISTERESIS
s = prs.slides.add_slide(BLANK)
base(s, "09  ·  Hasil", "Histeresis & repeatability: dua sumber galat berbeda",
     "Kedua parameter diukur dari tiga siklus penuh naik–turun pada 11 titik tekanan.")
picture(s, "05_histeresis_repeatability.png", 1.76, max_w=12.20, max_h=4.05)
for i, (v, l, c) in enumerate([
        ("0,06 % FS", "histeresis maksimum (6 mbar)", TEAL),
        ("0,016 % FS", "repeatability (1,6 mbar)", TEAL),
        ("3 siklus", "pengulangan tiap titik ukur", AMBER)]):
    metric(s, 0.62 + i * 4.12, 5.72, 3.86, 1.08, v, l, c)
footer(s, 10)

# ================================================================== 11. KETIDAKPASTIAN
s = prs.slides.add_slide(BLANK)
base(s, "10  ·  Analisis", "Anggaran ketidakpastian: U = 8,2 mbar (0,082 % FS)",
     "Kontribusi dominan adalah resolusi DUT itu sendiri, bukan sistem kalibratornya.")
picture(s, "06_ketidakpastian.png", 1.74, max_w=12.20, max_h=4.35)
note(s, 0.62, 6.28, 12.12,
     "Rasio TUR 6,1 : 1 melebihi syarat minimum 4 : 1 (ANSI/ISA-51.1) — sistem layak dipakai sebagai kalibrator kerja.")
footer(s, 11)

# ================================================================== 12. KESIMPULAN
s = prs.slides.add_slide(BLANK)
base(s, "11  ·  Penutup", "Kesimpulan & rencana lanjutan",
     "Rancangan memenuhi target; tahap berikutnya fabrikasi dan validasi eksperimental.")

tb(s, 0.62, 1.86, 6.15, 0.28, "KESIMPULAN SEMENTARA", 9.8, TEAL, True, FONT_B)
bullets(s, 0.62, 2.22, 6.20, [
    ("Otomasi 63 titik dalam ≈ 21 menit", "vs ± 45 menit manual per sensor"),
    ("Galat sistematis terkompensasi", "0,22 % → 0,03 % FS dengan koreksi 2 titik"),
    ("Ketidakpastian U = 0,082 % FS", "TUR 6,1 : 1, layak sebagai kalibrator kerja"),
    ("Jejak audit digital", "setiap sampel tersimpan di basis data"),
], size=12.2, gap=0.40, sub_size=9.8)

tb(s, 7.05, 1.86, 5.7, 0.28, "RENCANA 8 MINGGU", 9.8, AMBER, True, FONT_B)
picture(s, "09_roadmap.png", 2.16, max_w=5.72, max_h=2.62, left=7.02)

rect(s, 7.05, 4.86, 5.68, 1.55, fill=NAVY, line=None)
tb(s, 7.32, 5.04, 5.1, 0.28, "RISIKO UTAMA & MITIGASI", 9.5, AMBER, True, FONT_B)
tb(s, 7.32, 5.38, 5.15, 0.90,
   "Kebocoran ruang uji → uji tekan 10 menit sebelum kalibrasi.\n"
   "Drift suhu referensi → kalibrasi silang harian dan catat suhu ruang.",
   10.2, WHITE, False, FONT, spacing=1.30)

tb(s, 0.62, 5.20, 6.15, 0.30, "Terima kasih — kami siap menerima pertanyaan.", 13,
   NAVY, True, FONT_B)
tb(s, 0.62, 5.56, 6.15, 0.55,
   "Kelompok 3  ·  [Nama 1] · [Nama 2] · [Nama 3]", 11, GRAY, False, FONT)
footer(s, 12)

prs.save(OUT)
print("saved:", OUT)
print("slides:", len(prs.slides.__iter__.__self__._sldIdLst))
