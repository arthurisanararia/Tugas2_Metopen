# -*- coding: utf-8 -*-
"""
Generator aset visualisasi presentasi:
"Rancang Bangun Sistem Kalibrasi Otomatis Sensor Tekanan
 Menggunakan Transduser Referensi Standar"
Output: assets/png/*.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "png")
os.makedirs(OUT, exist_ok=True)

NAVY = "#0F2A44"
NAVY2 = "#1B3F63"
TEAL = "#0E9F8E"
TEAL_L = "#D7F0EC"
AMBER = "#E39A28"
RED = "#C9463D"
GRAY = "#6B7A8A"
LGRAY = "#E8EDF2"
BG = "#FFFFFF"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": "#B9C4CF",
    "axes.labelcolor": NAVY,
    "text.color": NAVY,
    "xtick.color": GRAY,
    "ytick.color": GRAY,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "figure.facecolor": BG,
    "savefig.facecolor": BG,
    "axes.grid": False,
})


def clean(ax, grid=True):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#B9C4CF")
    ax.spines["bottom"].set_color("#B9C4CF")
    if grid:
        ax.grid(True, color="#E8EDF2", lw=0.9, zorder=0)
        ax.set_axisbelow(True)


def save(fig, name, dpi=220):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=dpi, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print("ok:", p)


def box(ax, x, y, w, h, title, sub="", fc="white", ec=NAVY, tc=NAVY, fs=10.5,
        sfs=8.6, lw=1.6, r=0.10):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0.02,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, zorder=3))
    if sub:
        ax.text(x + w / 2, y + h * 0.63, title, ha="center", va="center",
                fontsize=fs, color=tc, fontweight="bold", zorder=4)
        ax.text(x + w / 2, y + h * 0.27, sub, ha="center", va="center",
                fontsize=sfs, color=tc if tc != NAVY else GRAY, zorder=4)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center",
                fontsize=fs, color=tc, fontweight="bold", zorder=4)


def arrow(ax, p1, p2, color=NAVY, lw=1.9, style="-|>", ls="-", rad=0.0, ms=14):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, linestyle=ls, zorder=2,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=2, shrinkB=2))


def path(ax, pts, color=NAVY, lw=1.9, head=True, ms=14):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round",
            solid_joinstyle="round", zorder=2)
    if head:
        ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>",
                                     mutation_scale=ms, color=color, lw=lw, zorder=2))


# ================================================================ 1. BLOCK DIAGRAM
def fig_block():
    fig, ax = plt.subplots(figsize=(13.0, 7.0))
    ax.set_xlim(-0.45, 16.1)
    ax.set_ylim(0, 9.0)
    ax.axis("off")

    ax.text(7.8, 8.70, "Arsitektur sistem kalibrasi otomatis", fontsize=16,
            fontweight="bold", ha="center", va="center", color=NAVY)

    ax.text(-0.28, 6.35, "JALUR PNEUMATIK", rotation=90, fontsize=8.8,
            color=TEAL, fontweight="bold", ha="center", va="center")
    ax.text(-0.28, 1.40, "JALUR SINYAL & KENDALI", rotation=90, fontsize=8.8,
            color=AMBER, fontweight="bold", ha="center", va="center")

    # ---- baris pneumatik
    box(ax, 0.25, 5.55, 2.45, 1.55, "Kompresor", "udara kering\n6–8 bar", fc=LGRAY)
    box(ax, 3.10, 5.55, 2.45, 1.55, "Filter–Regulator", "+ katup jarum\n0–10 bar", fc=LGRAY)
    box(ax, 5.95, 5.45, 3.05, 1.75, "Manifold + 3 Katup", "kasar / halus / vent",
        fc=TEAL_L, ec=TEAL)
    box(ax, 9.40, 5.45, 2.95, 1.75, "Ruang Uji", "V ≈ 120 mL\nDUT + referensi",
        fc=TEAL_L, ec=TEAL)
    box(ax, 12.85, 5.98, 2.50, 0.68, "Vent → atmosfer", fc="white", ec=GRAY,
        tc=GRAY, fs=8.8)

    arrow(ax, (2.70, 6.32), (3.10, 6.32))
    arrow(ax, (5.55, 6.32), (5.95, 6.32))
    arrow(ax, (9.00, 6.32), (9.40, 6.32))
    arrow(ax, (12.35, 6.32), (12.85, 6.32), color=GRAY)

    # ---- transduser
    box(ax, 9.40, 3.90, 2.95, 0.95, "DUT  ·  0–10 bar", fc="white",
        ec=AMBER, tc=AMBER, fs=9.2)
    box(ax, 12.75, 3.90, 2.60, 0.95, "Transduser referensi", "akurasi 0,02 % FS",
        fc="white", ec=AMBER, tc=AMBER, fs=8.2, sfs=7.6)
    arrow(ax, (10.30, 5.45), (10.30, 4.85), color=AMBER, lw=1.5, ms=12)
    ax.text(10.42, 5.15, "P", fontsize=9, color=AMBER, fontweight="bold")
    path(ax, [(12.05, 5.45), (12.05, 4.38), (12.75, 4.38)], color=AMBER, lw=1.5, ms=12)
    ax.text(12.17, 5.15, "P", fontsize=9, color=AMBER, fontweight="bold")

    # ---- baris sinyal
    box(ax, 0.25, 0.55, 2.55, 1.55, "Pengkondisi Sinyal", "INA333 · G = 100\nRC 1,6 kHz + LPF 2 Hz",
        fs=9.6)
    box(ax, 3.30, 0.55, 2.45, 1.55, "ADC 24-bit", "ADS1256 · PGA 32", fs=9.8)
    box(ax, 6.25, 0.55, 2.55, 1.55, "Mikrokontroler", "ESP32-S3\nPI + penjadwal",
        fc=NAVY, ec=NAVY, tc="white", fs=9.8)
    box(ax, 9.30, 0.55, 2.65, 1.55, "GUI & Basis Data", "Python · SQLite\nlaporan PDF", fs=9.6)
    box(ax, 12.45, 0.55, 2.85, 1.55, "Driver Katup", "MOSFET + flyback\nPWM 1 kHz",
        fc=LGRAY, fs=9.6)

    arrow(ax, (2.80, 1.32), (3.30, 1.32))
    arrow(ax, (5.75, 1.32), (6.25, 1.32))
    arrow(ax, (8.80, 1.32), (9.30, 1.32))
    arrow(ax, (11.95, 1.32), (12.45, 1.32), style="<|-|>", ms=12)

    # DUT -> pengkondisi sinyal
    path(ax, [(9.40, 4.68), (0.60, 4.68), (0.60, 2.35), (1.30, 2.35)], color=AMBER, lw=1.5)
    ax.text(3.20, 4.82, "sinyal DUT  (mV)", fontsize=8.4, color=AMBER, style="italic")

    # referensi -> ADC
    path(ax, [(15.35, 4.38), (15.35, 3.30), (4.55, 3.30), (4.55, 2.35)], color=AMBER, lw=1.5)
    ax.text(6.30, 3.42, "sinyal referensi 0–5 V", fontsize=8.4, color=AMBER, style="italic")

    # driver -> manifold
    path(ax, [(15.30, 2.10), (15.75, 2.10), (15.75, 7.55), (7.45, 7.55), (7.45, 7.20)],
         color=RED, lw=1.7)
    ax.text(15.90, 5.60, "aktuasi katup", rotation=90, fontsize=8.0, color=RED,
            ha="center", va="center")

    # umpan balik
    arrow(ax, (7.50, 2.10), (7.50, 3.80), color=GRAY, lw=1.2, ls=(0, (4, 3)), ms=12)
    ax.text(7.65, 2.95, "umpan balik\ntekanan", fontsize=7.8, color=GRAY, va="center")
    ax.text(7.50, 0.30, "setpoint P(t) → PI → duty katup", fontsize=8.4, color="white",
            ha="center")

    save(fig, "01_diagram_blok.png")


# ================================================================ 2. P&ID
def fig_pid():
    fig, ax = plt.subplots(figsize=(12.8, 6.0))
    ax.set_xlim(-0.2, 16.2)
    ax.set_ylim(-0.6, 7.5)
    ax.axis("off")

    def valve(x, y, tag, note):
        ax.add_patch(Polygon([[x - 0.34, y - 0.26], [x, y], [x - 0.34, y + 0.26]],
                             closed=True, fc="white", ec=NAVY, lw=1.8, zorder=4))
        ax.add_patch(Polygon([[x + 0.34, y - 0.26], [x, y], [x + 0.34, y + 0.26]],
                             closed=True, fc="white", ec=NAVY, lw=1.8, zorder=4))
        ax.plot([x, x], [y + 0.26, y + 0.50], color=NAVY, lw=1.6, zorder=3)
        ax.plot([x - 0.16, x + 0.16], [y + 0.50, y + 0.50], color=NAVY, lw=1.6, zorder=3)
        ax.text(x, y + 0.60, tag, ha="center", va="bottom", fontsize=9.0,
                color=NAVY, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))

    def instr(x, y, tag, label, color=TEAL):
        ax.add_patch(Circle((x, y), 0.36, fc="white", ec=color, lw=1.8, zorder=5))
        ax.text(x, y, tag, ha="center", va="center", fontsize=8.4, fontweight="bold",
                color=color, zorder=6)
        ax.text(x, y - 0.58, label, ha="center", va="top", fontsize=7.8, color=GRAY)

    def pipe(pts, lw=2.2, color=NAVY2):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round",
                solid_joinstyle="round", zorder=1)

    ax.text(0.1, 7.05, "Skematik pneumatik (P&ID sederhana)", fontsize=15,
            fontweight="bold", color=NAVY)

    # ---- kompresor + filter-regulator + indikator
    ax.add_patch(Circle((1.35, 4.55), 0.62, fc=LGRAY, ec=NAVY, lw=1.8, zorder=4))
    ax.add_patch(Polygon([[1.05, 4.25], [1.05, 4.85], [1.55, 4.55]], closed=True,
                         fc=NAVY, ec=NAVY, zorder=5))
    ax.text(1.35, 3.62, "M1  Kompresor", ha="center", fontsize=8.8,
            fontweight="bold", color=NAVY)
    ax.text(1.35, 3.32, "6–8 bar, 25 L/min", ha="center", fontsize=7.6, color=GRAY)

    pipe([(1.97, 4.55), (2.60, 4.55)])
    ax.add_patch(Polygon([[2.60, 4.15], [3.25, 4.15], [3.25, 4.95], [2.60, 4.95]],
                         closed=True, fc="white", ec=NAVY, lw=1.8, zorder=4))
    ax.plot([2.60, 3.25], [4.30, 4.80], color=NAVY, lw=1.2, zorder=5)
    ax.text(2.93, 3.62, "FIL-REG", ha="center", fontsize=8.4, fontweight="bold", color=NAVY)
    ax.text(2.93, 3.32, "5 µm + 0–10 bar", ha="center", fontsize=7.6, color=GRAY)

    pipe([(3.25, 4.55), (4.00, 4.55)])
    instr(4.35, 4.55, "PI", "indikator tekanan")

    # ---- manifold suplai (hanya untuk SV1 & SV2)
    pipe([(4.71, 4.55), (5.30, 4.55), (5.30, 5.55), (8.05, 5.55)])
    ax.text(5.42, 5.72, "manifold suplai", fontsize=7.8, color=GRAY, va="bottom")

    # ---- ruang uji
    ax.add_patch(FancyBboxPatch((5.40, 1.15), 5.40, 1.90,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=TEAL_L, ec=TEAL, lw=2.0, zorder=3))
    ax.text(8.10, 2.63, "RUANG UJI  ·  V = 120 mL", ha="center", fontsize=9.4,
            fontweight="bold", color=TEAL, zorder=4)
    ax.text(8.10, 2.13, "tekanan seragam, bocor < 0,5 mbar/menit", ha="center",
            fontsize=8.0, color=GRAY, zorder=4)
    ax.text(8.10, 1.66, "uji kebocoran 10 menit @ 10 bar", ha="center",
            fontsize=8.0, color=GRAY, zorder=4)

    # ---- SV1 (kasar) & SV2 (halus) : manifold -> ruang uji
    for x, tag, note in [(6.05, "SV1", "kasar"),
                         (7.45, "SV2", "halus")]:
        valve(x, 4.35, tag, note)
        pipe([(x, 5.55), (x, 4.61)], lw=2.0)
        pipe([(x, 4.09), (x, 3.05)], lw=2.0)

    # ---- SV3 (vent) : ruang uji -> atmosfer
    valve(9.85, 4.45, "SV3", "vent")
    pipe([(9.85, 3.05), (9.85, 4.19)], lw=2.0)
    pipe([(9.85, 4.71), (9.85, 6.35), (12.30, 6.35)], lw=2.0)
    ax.plot([12.30, 12.30], [6.10, 6.60], color=NAVY2, lw=2.2)
    ax.plot([12.45, 12.45], [6.10, 6.60], color=NAVY2, lw=2.2)
    ax.text(12.38, 6.78, "ke atmosfer", ha="center", fontsize=7.8, color=GRAY)

    # ---- instrumen pada ruang uji
    pipe([(7.20, 1.15), (7.20, 0.80)], lw=2.0)
    instr(7.20, 0.50, "PT-100", "DUT (0–10 bar)", AMBER)
    pipe([(9.00, 1.15), (9.00, 0.80)], lw=2.0)
    instr(9.00, 0.50, "PT-101", "referensi 0,02 % FS", AMBER)

    ax.text(0.1, -0.55, "SV1 = kasar (naik cepat)   ·   SV2 = halus (kontrol presisi, seri dengan katup jarum)"
                        "   ·   SV3 = vent (turunkan tekanan)", fontsize=8.4, color=GRAY)
    save(fig, "02_skematik_pneumatik.png")


# ================================================================ 3. SIGNAL CHAIN
def fig_signal():
    fig, ax = plt.subplots(figsize=(12.8, 5.4))
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0.4, 6.2)
    ax.axis("off")

    ax.text(0.1, 5.85, "Rantai sinyal dan anggaran resolusi", fontsize=15,
            fontweight="bold", color=NAVY)

    def wire(pts, color=NAVY2, lw=1.9):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round",
                solid_joinstyle="round", zorder=1)

    # jembatan wheatstone
    cx, cy, r = 1.55, 3.30, 0.80
    ax.add_patch(Polygon([[cx, cy + r], [cx + r, cy], [cx, cy - r], [cx - r, cy]],
                         closed=True, fc="white", ec=NAVY, lw=1.8, zorder=3))
    for dx, dy, lab in [(0, 0.43, "R1"), (0.43, 0, "R2"), (0, -0.43, "R3"), (-0.43, 0, "R4")]:
        ax.text(cx + dx, cy + dy, lab, ha="center", va="center", fontsize=8.2,
                color=GRAY, zorder=4)
    ax.text(cx, 1.85, "jembatan piezoresistif\n350 Ω, eksitasi 5 V", ha="center",
            fontsize=7.8, color=GRAY, va="top")

    def amp(x, y, w, h, name, sub, ec=TEAL):
        ax.add_patch(Polygon([[x, y - h / 2], [x, y + h / 2], [x + w, y]],
                             closed=True, fc="white", ec=ec, lw=1.8, zorder=3))
        ax.text(x + w * 0.40, y + 0.42, name, fontsize=8.6, fontweight="bold",
                color=NAVY, zorder=4)
        ax.text(x + w * 0.40, y - 0.46, sub, fontsize=7.4, color=GRAY, zorder=4)

    wire([(2.35, 3.90), (3.10, 3.90), (3.10, 3.72)])
    wire([(2.35, 2.70), (3.10, 2.70), (3.10, 2.88)])
    amp(3.10, 3.30, 1.60, 1.50, "INA333", "G = 100")
    ax.text(3.24, 3.96, "–", fontsize=12, color=NAVY, va="center")
    ax.text(3.24, 2.64, "+", fontsize=11, color=NAVY, va="center")

    # RC low-pass
    wire([(4.70, 3.30), (5.15, 3.30)])
    ax.add_patch(Rectangle((5.15, 3.10), 0.75, 0.40, fc="white", ec=NAVY, lw=1.6, zorder=3))
    ax.text(5.525, 3.30, "1 k", ha="center", va="center", fontsize=7.6, color=GRAY, zorder=4)
    ax.plot([5.90, 7.10], [3.30, 3.30], color=NAVY2, lw=1.9, zorder=1)
    ax.plot([6.45, 6.45], [3.30, 2.80], color=NAVY2, lw=1.9, zorder=1)
    ax.plot([6.28, 6.62], [2.80, 2.80], color=NAVY2, lw=2.8, zorder=1)
    ax.plot([6.28, 6.62], [2.63, 2.63], color=NAVY2, lw=2.8, zorder=1)
    ax.text(6.45, 2.45, "100 nF", ha="center", va="top", fontsize=7.4, color=GRAY)
    ax.text(6.45, 2.05, "$f_c$ ≈ 1,6 kHz", ha="center", va="top", fontsize=7.4, color=GRAY)

    # ADC
    box(ax, 7.10, 2.20, 2.10, 2.20, "", fc=NAVY, ec=NAVY)
    ax.text(8.15, 3.92, "ADS1256", ha="center", fontsize=9.4, fontweight="bold", color="white")
    ax.text(8.15, 3.48, "24-bit  ΔΣ", ha="center", fontsize=8.2, color="#CFE3F5")
    ax.text(8.15, 3.04, "PGA = 32", ha="center", fontsize=8.2, color="#CFE3F5")
    ax.text(8.15, 2.60, "30 kSPS", ha="center", fontsize=8.2, color="#CFE3F5")

    for i, lab in enumerate(["SCLK", "DIN", "DOUT", "DRDY"]):
        yy = 3.90 - i * 0.44
        ax.plot([9.20, 10.30], [yy, yy], color=TEAL, lw=1.4, zorder=1)
        ax.text(9.75, yy + 0.12, lab, fontsize=6.6, color=TEAL, ha="center")
    ax.text(9.75, 4.32, "SPI", fontsize=7.6, color=TEAL, ha="center", fontweight="bold")

    box(ax, 10.30, 2.20, 2.10, 2.20, "", fc="white", ec=NAVY, lw=1.8)
    ax.text(11.35, 3.92, "ESP32-S3", ha="center", fontsize=9.4, fontweight="bold", color=NAVY)
    ax.text(11.35, 3.48, "240 MHz", ha="center", fontsize=8.2, color=GRAY)
    ax.text(11.35, 3.04, "PI 10 Hz", ha="center", fontsize=8.2, color=GRAY)
    ax.text(11.35, 2.60, "Wi-Fi + SD", ha="center", fontsize=8.2, color=GRAY)

    ax.add_patch(FancyArrowPatch((12.40, 3.30), (13.10, 3.30), arrowstyle="-|>",
                                 mutation_scale=13, color=NAVY, lw=1.8, zorder=2))
    ax.text(12.75, 3.05, "UART", fontsize=6.8, color=GRAY, ha="center", va="top")

    box(ax, 13.10, 2.35, 2.80, 1.90, "GUI Python", "kurva · tabel · laporan\nSQLite + PDF",
        fc=LGRAY, ec=GRAY)

    ax.text(0.1, 1.05, "Resolusi efektif 10 bar / 2$^{24}$ ≈ 0,6 µbar   →   derau input 1,2 µV rms ≈ 0,3 mbar"
                       "   →   jauh di bawah resolusi DUT (10 mbar)", fontsize=8.8, color=NAVY)
    ax.text(0.1, 0.62, "CMC sistem ditentukan oleh transduser referensi + repeatability, bukan oleh ADC.",
            fontsize=8.8, color=GRAY, style="italic")
    save(fig, "03_rantai_sinyal.png")


# ================================================================ 4. CALIBRATION CURVE
def fig_calibration():
    rng = np.random.default_rng(7)
    P = np.arange(0, 11, 1.0)
    FS = 10.0

    def ind(p, direction=1):
        gain, off = 0.9965, 0.021
        nl = 0.0022 * np.sin(np.pi * p / FS * 1.6) + 0.0008 * (p / FS) ** 2
        hy = 0.0030 * direction * (1 - np.abs(p / FS - 0.5) * 1.2)
        return gain * p + off + nl + hy + rng.normal(0, 0.0009, p.shape)

    up = ind(P, +1)
    down = ind(P, -1)

    A = np.vstack([P, np.ones_like(P)]).T
    (a, b), *_ = np.linalg.lstsq(A, up, rcond=None)

    fig, axs = plt.subplots(1, 2, figsize=(13.2, 4.9),
                            gridspec_kw={"width_ratios": [1, 1.1]})

    ax = axs[0]
    ax.plot([0, 10], [0, 10], color=GRAY, lw=1.4, ls="--", label="ideal (1:1)", zorder=2)
    ax.plot(P, up, "o-", color=AMBER, lw=1.8, ms=5.5, label="DUT (naik)", zorder=4)
    ax.plot(P, down, "s--", color=TEAL, lw=1.5, ms=4.5, mfc="white", label="DUT (turun)", zorder=3)
    ax.set_xlabel("Tekanan referensi  $P_{ref}$  [bar]")
    ax.set_ylabel("Pembacaan DUT  [bar]")
    ax.set_title("Kurva kalibrasi 0–10 bar, 11 titik")
    ax.set_xlim(-0.4, 10.4)
    ax.set_ylim(-0.4, 10.4)
    ax.legend(frameon=False, fontsize=8.6, loc="upper left")
    ax.text(0.97, 0.06, f"$P_{{ind}}$ = {a:.4f}·$P_{{ref}}$ + {b:.4f}",
            transform=ax.transAxes, ha="right", fontsize=9.4, color=NAVY,
            bbox=dict(boxstyle="round,pad=0.35", fc=LGRAY, ec="none"))
    clean(ax)

    ax = axs[1]
    e_before = (up - P) / FS * 100
    e_after = ((up - b) / a - P) / FS * 100
    ax.axhspan(-0.1, 0.1, color=TEAL_L, zorder=0)
    ax.axhline(0, color=GRAY, lw=1.0)
    ax.plot(P, e_before, "o-", color=RED, lw=1.8, ms=5, label="sebelum koreksi")
    ax.plot(P, e_after, "s-", color=TEAL, lw=1.8, ms=5, label="setelah koreksi 2 titik")
    ax.set_xlabel("Tekanan referensi  $P_{ref}$  [bar]")
    ax.set_ylabel("Galat  [% FS]")
    ax.set_title("Galat terhadap referensi")
    ax.set_xlim(-0.4, 10.4)
    ax.set_ylim(-0.42, 0.42)
    ax.legend(frameon=False, fontsize=8.6, loc="lower left")
    ax.text(0.35, 0.115, "pita sasaran ±0,1 % FS", fontsize=8.0, color=TEAL)
    ax.annotate(f"maks {np.abs(e_before).max():.2f} % FS",
                xy=(P[np.argmax(np.abs(e_before))], e_before.max()),
                xytext=(1.2, 0.33), fontsize=8.2, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
    ax.annotate(f"maks {np.abs(e_after).max():.2f} % FS",
                xy=(P[np.argmax(np.abs(e_after))], e_after.max()),
                xytext=(6.4, 0.30), fontsize=8.2, color=TEAL,
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.0))
    clean(ax)

    fig.tight_layout(w_pad=2.4)
    save(fig, "04_kurva_kalibrasi.png")


# ================================================================ 5. HYSTERESIS
def fig_hyst():
    rng = np.random.default_rng(21)
    P = np.arange(0, 11, 1.0)
    FS = 10.0

    def cyc(direction, shift=0.0, noise=0.0004):
        nl = 0.0022 * np.sin(np.pi * P / FS * 1.6) + 0.0008 * (P / FS) ** 2
        hy = -0.0030 * direction * np.sin(np.pi * P / FS)
        return 0.9965 * P + 0.021 + nl + hy + rng.normal(0, noise, P.shape) + shift

    up = np.mean([cyc(+1) for _ in range(3)], axis=0)
    down = np.mean([cyc(-1) for _ in range(3)], axis=0)
    # garis dasar = regresi kuadratik pada siklus naik,
    # agar yang tersisa hanya histeresis (bukan nonlinearitas statis)
    A = np.vstack([P ** 2, P, np.ones_like(P)]).T
    (a2, a1, a0), *_ = np.linalg.lstsq(A, up, rcond=None)
    base = a2 * P ** 2 + a1 * P + a0

    fig, axs = plt.subplots(1, 2, figsize=(13.2, 4.7))

    ax = axs[0]
    eu = (up - base) / FS * 100
    ed = (down - base) / FS * 100
    ax.plot(P, eu, "o-", color=AMBER, lw=1.9, ms=5.5, label="naik")
    ax.plot(P, ed, "s-", color=TEAL, lw=1.9, ms=5, label="turun")
    ax.fill_between(P, ed, eu, color=AMBER, alpha=0.16)
    ax.axhline(0, color=GRAY, lw=1.0)
    ax.set_xlabel("Tekanan referensi  [bar]")
    ax.set_ylabel("Galat terhadap garis dasar  [% FS]")
    ax.set_title("Histeresis  (rata-rata 3 siklus)")
    ax.set_ylim(-0.075, 0.075)
    ax.legend(frameon=False, fontsize=8.8, loc="lower left")
    ax.text(0.97, 0.93, f"histeresis maks = {np.max(np.abs(eu-ed)):.3f} % FS",
            transform=ax.transAxes, ha="right", va="top", fontsize=9.2, color=NAVY,
            bbox=dict(boxstyle="round,pad=0.32", fc=LGRAY, ec="none"))
    clean(ax)

    ax = axs[1]
    colors = [NAVY, TEAL, AMBER]
    data = np.array([cyc(+1, rng.normal(0, 0.0006), 0.0005) for _ in range(3)])
    for k in range(3):
        ax.plot(P, (data[k] - base) / FS * 100, "o-", color=colors[k], lw=1.5, ms=4.2,
                label=f"siklus {k+1}")
    m = (data.mean(0) - base) / FS * 100
    s = data.std(0, ddof=1) / FS * 100
    ax.fill_between(P, m - s, m + s, color=GRAY, alpha=0.18, lw=0)
    ax.axhline(0, color=GRAY, lw=1.0)
    ax.set_xlabel("Tekanan referensi  [bar]")
    ax.set_ylabel("Galat terhadap garis dasar  [% FS]")
    ax.set_title("Repeatability 3 siklus")
    ax.set_ylim(-0.075, 0.075)
    ax.legend(frameon=False, fontsize=8.4, loc="lower left", ncol=3)
    ax.text(0.97, 0.93, f"$s_{{maks}}$ = {s.max():.3f} % FS", transform=ax.transAxes,
            ha="right", va="top", fontsize=9.2, color=NAVY,
            bbox=dict(boxstyle="round,pad=0.32", fc=LGRAY, ec="none"))
    clean(ax)

    fig.tight_layout(w_pad=2.4)
    save(fig, "05_histeresis_repeatability.png")


# ================================================================ 6. UNCERTAINTY
def fig_unc():
    comp = [
        ("Referensi 0,02 % FS", 2.0 / np.sqrt(3), TEAL),
        ("Resolusi DUT 10 mbar", 10.0 / (2 * np.sqrt(3)), NAVY),
        ("Repeatability $s/\\sqrt{n}$", 1.6 / np.sqrt(3), AMBER),
        ("Histeresis 6 mbar", 6.0 / (2 * np.sqrt(3)), "#7A8FA6"),
        ("Linearitas sisa 3 mbar", 3.0 / np.sqrt(3), "#9AA9B8"),
        ("Drift suhu 1 mbar", 1.0 / np.sqrt(3), "#B6C1CC"),
    ]
    u = np.array([c[1] for c in comp])
    uc = np.sqrt((u ** 2).sum())
    U = 2 * uc

    fig, axs = plt.subplots(1, 2, figsize=(13.4, 4.9),
                            gridspec_kw={"width_ratios": [1.3, 1]})

    ax = axs[0]
    labels = [c[0] for c in comp][::-1]
    vals = u[::-1]
    cols = [c[2] for c in comp][::-1]
    y = np.arange(len(vals))
    ax.barh(y, vals, color=cols, height=0.62, zorder=3)
    for yi, v in zip(y, vals):
        ax.text(v + 0.09, yi, f"{v:.2f}", va="center", fontsize=8.6, color=NAVY)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8.8)
    ax.set_xlabel("Kontribusi ketidakpastian  $u_i$  [mbar]")
    ax.set_title("Anggaran ketidakpastian @ 10 bar")
    ax.set_xlim(0, max(vals) * 1.30)
    ax.axvline(uc, color=RED, lw=1.3, ls="--", zorder=4)
    ax.text(uc + 0.07, len(vals) - 0.55, f"$u_c$ = {uc:.2f} mbar", color=RED, fontsize=8.8,
            va="center", ha="left")
    clean(ax, grid=False)

    ax = axs[1]
    rel = (u ** 2) / (u ** 2).sum() * 100
    order = np.argsort(rel)[::-1]
    ax.pie(rel[order], colors=[comp[i][2] for i in order], startangle=90,
           counterclock=False,
           wedgeprops=dict(width=0.42, edgecolor="white", lw=1.6))
    ax.text(0, 0.12, f"$U$ = {U:.2f} mbar", ha="center", fontsize=12.5,
            fontweight="bold", color=NAVY)
    ax.text(0, -0.16, f"= {U/100:.3f} % FS   (k = 2)", ha="center", fontsize=9.4, color=GRAY)
    ax.set_title("Kontribusi relatif  $u_i^2$")
    ax.legend([f"{comp[i][0]}  {rel[i]:.0f}%" for i in order[:4]], loc="center left",
              bbox_to_anchor=(0.98, 0.5), frameon=False, fontsize=7.8, handlelength=1.0)

    tur = 0.5 / (U / 100)
    fig.text(0.5, -0.05, f"TUR terhadap DUT kelas 0,5 % FS  =  0,5 % / {U/100:.3f} %  ≈  {tur:.1f} : 1"
                         "   →  memenuhi ANSI/ISA-51.1 (≥ 4 : 1)", ha="center",
             fontsize=9.4, color=NAVY)
    fig.tight_layout(w_pad=1.0)
    save(fig, "06_ketidakpastian.png")


# ================================================================ 7. FLOWCHART
def fig_flow():
    fig, ax = plt.subplots(figsize=(13.0, 7.0))
    ax.set_xlim(0, 16.6)
    ax.set_ylim(-0.4, 10.4)
    ax.axis("off")

    ax.text(0.15, 10.05, "Alur perangkat lunak kalibrasi otomatis", fontsize=15,
            fontweight="bold", color=NAVY)

    def node(x, y, w, h, text, kind="proc", fs=8.8):
        if kind == "term":
            ax.add_patch(FancyBboxPatch((x, y), w, h,
                                        boxstyle=f"round,pad=0.02,rounding_size={h/2}",
                                        fc=NAVY, ec=NAVY, lw=1.6, zorder=3))
            tc = "white"
        elif kind == "dec":
            ax.add_patch(Polygon([[x + w / 2, y + h], [x + w, y + h / 2],
                                  [x + w / 2, y], [x, y + h / 2]], closed=True,
                                 fc=AMBER, ec=AMBER, lw=1.6, zorder=3))
            tc = "white"
        elif kind == "io":
            ax.add_patch(FancyBboxPatch((x, y), w, h,
                                        boxstyle="round,pad=0.02,rounding_size=0.10",
                                        fc=TEAL_L, ec=TEAL, lw=1.6, zorder=3))
            tc = NAVY
        else:
            ax.add_patch(FancyBboxPatch((x, y), w, h,
                                        boxstyle="round,pad=0.02,rounding_size=0.10",
                                        fc="white", ec=NAVY, lw=1.6, zorder=3))
            tc = NAVY
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
                color=tc, zorder=4, linespacing=1.45)

    X, W = 4.70, 4.40
    cx = X + W / 2

    node(X, 8.75, W, 0.68, "MULAI  ·  inisialisasi & zeroing", "term", 8.6)
    node(X, 7.35, W, 0.90, "Muat konfigurasi\n(rentang, titik, siklus)", "io")
    node(X, 5.95, W, 0.90, "Kendalikan tekanan ke setpoint\nPI 10 Hz · pilih katup kasar/halus")
    node(X - 0.45, 4.35, W + 0.90, 1.15, "Stabil?\n|e| < 0,02 % FS selama 2 s", "dec", 8.2)
    node(X, 2.90, W, 0.90, "Akuisisi 1 000 sampel\nrata-rata + simpangan baku")
    node(X, 1.45, W, 0.90, "Simpan (P_ref, P_ind)\nke basis data", "io")
    node(11.15, 2.55, 3.10, 1.60, "Titik &\nsiklus\nselesai?", "dec", 8.2)
    node(10.90, 0.10, 5.60, 1.00, "Regresi · histeresis · repeatability\nanggaran U  →  laporan PDF",
         "io", 8.4)

    for y1, y2 in [(8.75, 8.25), (7.35, 6.85), (5.95, 5.50)]:
        arrow(ax, (cx, y1), (cx, y2), ms=12)

    # loop "tidak" (dekat, amber)
    ax.plot([X - 0.45, 3.95], [4.92, 4.92], color=AMBER, lw=1.6, zorder=2)
    ax.plot([3.95, 3.95], [4.92, 6.62], color=AMBER, lw=1.6, zorder=2)
    arrow(ax, (3.95, 6.62), (X, 6.62), color=AMBER, lw=1.6, ms=12)
    ax.text(4.12, 5.55, "tidak", fontsize=8.2, color=AMBER, fontweight="bold",
            rotation=90, va="center", ha="left")

    arrow(ax, (cx, 4.35), (cx, 3.80), ms=12)
    arrow(ax, (cx, 2.90), (cx, 2.35), ms=12)

    # simpan -> keputusan
    ax.plot([X + W, 9.95], [1.90, 1.90], color=NAVY2, lw=1.6, zorder=2)
    ax.plot([9.95, 9.95], [1.90, 3.35], color=NAVY2, lw=1.6, zorder=2)
    arrow(ax, (9.95, 3.35), (11.15, 3.35), color=NAVY2, lw=1.6, ms=12)

    # loop "titik berikutnya" (jauh, navy)
    ax.plot([cx, cx], [1.45, 0.90], color=NAVY2, lw=1.6, zorder=2)
    ax.plot([cx, 1.45], [0.90, 0.90], color=NAVY2, lw=1.6, zorder=2)
    ax.plot([1.45, 1.45], [0.90, 6.25], color=NAVY2, lw=1.6, zorder=2)
    arrow(ax, (1.45, 6.25), (X, 6.25), color=NAVY2, lw=1.6, ms=12)
    ax.text(1.62, 3.55, "titik berikutnya", fontsize=8.0, color=NAVY2, rotation=90,
            va="center", ha="left")

    # "ya"
    arrow(ax, (12.70, 2.55), (12.70, 1.10), color=TEAL, lw=1.7, ms=12)
    ax.text(12.85, 1.80, "ya", fontsize=8.4, color=TEAL, fontweight="bold")

    ax.text(0.15, 0.35, "63 titik ukur  =  11 titik × 3 siklus  ≈  21 menit per sensor",
            fontsize=8.6, color=GRAY, va="center")
    save(fig, "07_flowchart.png")


# ================================================================ 8. STEP RESPONSE
def fig_step():
    t = np.linspace(0, 26, 2601)
    sp = 6.0
    K, tau, L = 8.6, 0.9, 0.15
    dt = t[1] - t[0]
    y = np.zeros_like(t)
    y[0] = 0.02
    integ = 0.0
    Kp, Ti = 0.50, 2.5
    ubuf = np.zeros_like(t)
    nd = int(L / dt)
    for i in range(1, len(t)):
        e = sp - y[i - 1]
        integ += e * dt
        ubuf[i] = np.clip(Kp * (e + integ / Ti), 0, 1)
        u = ubuf[max(0, i - nd)]
        y[i] = y[i - 1] + dt / tau * (K * u - y[i - 1])

    os_pct = (y.max() / sp - 1) * 100
    bad = np.where(np.abs(y - sp) > 0.002 * sp)[0]
    ts = t[bad[-1] + 1]

    a0 = ts                     # mulai tunggu stabil
    a1 = ts + 2.0               # selesai tunggu stabil
    a2 = a1 + 6.0               # selesai akuisisi
    a3 = a2 + 10.0              # selesai pindah titik

    fig, ax = plt.subplots(figsize=(12.6, 5.2))
    ax.axhspan(sp * 0.998, sp * 1.002, color=TEAL_L, zorder=0)
    ax.axvspan(a0, a1, color=AMBER, alpha=0.16, zorder=1)
    ax.axvspan(a1, a2, color=TEAL, alpha=0.16, zorder=1)
    ax.axvspan(a2, a3, color=GRAY, alpha=0.11, zorder=1)

    ax.plot(t, y, color=NAVY, lw=2.2, zorder=4, label="tekanan ruang uji")
    ax.axhline(sp, color=TEAL, lw=1.4, ls="--", zorder=2, label="setpoint 6,000 bar")

    ax.set_xlabel("Waktu  [s]")
    ax.set_ylabel("Tekanan  [bar]")
    ax.set_xlim(0, 24)
    ax.set_ylim(4.85, 7.05)
    ax.set_title("Respons kendali tekanan pada satu titik ukur (PI, 10 Hz)")
    clean(ax)
    ax.legend(frameon=False, fontsize=8.4, loc="upper right", bbox_to_anchor=(1.0, 1.0))

    ax.text((a0 + a1) / 2, 4.94, "tunggu\nstabil", fontsize=7.2, color=AMBER,
            ha="center", va="bottom")
    ax.text((a1 + a2) / 2, 4.94, "akuisisi 1 000 sampel", fontsize=7.2, color=TEAL,
            ha="center", va="bottom")
    ax.text((a2 + a3) / 2, 4.94, "pindah titik\n(vent / naik)", fontsize=7.2, color=GRAY,
            ha="center", va="bottom")

    ax.annotate(f"overshoot {os_pct:.1f} %", xy=(t[np.argmax(y)], y.max()),
                xytext=(3.2, 6.62), fontsize=8.4, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
    ax.annotate(f"$t_s$ ≈ {ts:.1f} s  (pita ±0,2 % FS)", xy=(ts, sp * 1.002),
                xytext=(6.8, 6.42), fontsize=8.4, color=NAVY,
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.0))
    ax.text(0.985, 0.06, f"siklus per titik ≈ {a3:.0f} s  →  63 titik ≈ {63*a3/60:.0f} menit",
            transform=ax.transAxes, ha="right", fontsize=8.4, color=GRAY)
    save(fig, "08_respons_kendali.png")


# ================================================================ 9. GANTT
def fig_gantt():
    tasks = [
        ("Studi literatur & standar (ISO 17025, ISA-51.1)", 0, 2, TEAL, 100),
        ("Desain mekanik & rangkaian pneumatik", 1, 3, TEAL, 100),
        ("Desain elektronik & PCB akuisisi", 2, 3, TEAL, 100),
        ("Firmware ESP32 + GUI Python", 3, 4, AMBER, 70),
        ("Fabrikasi & perakitan", 4, 2, AMBER, 55),
        ("Uji kebocoran & karakterisasi", 5, 2, AMBER, 35),
        ("Kalibrasi & analisis ketidakpastian", 6, 2, LGRAY, 10),
        ("Laporan & publikasi", 7, 2, LGRAY, 0),
    ]
    fig, ax = plt.subplots(figsize=(12.8, 3.55))
    for i, (name, start, dur, col, prog) in enumerate(tasks):
        y = len(tasks) - 1 - i
        ax.barh(y, dur, left=start, height=0.58, color=col, alpha=0.26,
                edgecolor="none", zorder=2)
        ax.barh(y, dur * prog / 100, left=start, height=0.58, color=col,
                edgecolor="none", zorder=3)
        ax.text(start + dur + 0.13, y, f"{prog}%", va="center", fontsize=8.6, color=GRAY)
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([t[0] for t in tasks][::-1], fontsize=9.2)
    ax.set_xticks(range(0, 9))
    ax.set_xticklabels([f"M{i+1}" for i in range(9)], fontsize=9.0)
    ax.set_xlim(0, 9.8)
    ax.set_xlabel("Minggu pelaksanaan", fontsize=9.6)
    ax.axvline(5.0, color=RED, lw=1.7, ls="--", zorder=5)
    ax.text(5.10, len(tasks) - 0.28, "posisi sekarang\n(minggu ke-5)", fontsize=8.6,
            color=RED, va="top")
    ax.set_title("Jadwal pelaksanaan Tugas Akhir (8 minggu)", fontsize=11.5)
    ax.grid(True, axis="x", color="#E8EDF2", lw=0.9, zorder=0)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
    save(fig, "09_gantt.png")


if __name__ == "__main__":
    fig_block()
    fig_pid()
    fig_signal()
    fig_calibration()
    fig_hyst()
    fig_unc()
    fig_flow()
    fig_step()
    fig_gantt()
    print("SELESAI")
