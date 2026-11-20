"""Genera la plantilla imprimible per DIBUIXAR un fons 360 (graella equirectangular 2:1).

L'alumnat dibuixa dins el marc, l'escaneja o el fotografia, el retalla pel marc i el
puja com a «Imatge 360°» al constructor de mons (`proves/constructor-mons/`).

Dins el marc només hi ha línies molt clares perquè no destorbin el dibuix:
- graella cada 15° (més marcada cada 45°) i l'horitzó;
- guia d'una habitació vista des del centre (línies taronja discontínues): les arestes del
  terra, del sostre i dels racons. Mostra que les línies rectes surten corbades;
- les zones de dalt i de baix (més de 60°) ratllades: s'hi veu tot molt més petit.
Les etiquetes (davant, dreta, darrere…) queden fora del marc, al marge.

Ús:  py -3.11 eines/genera_graella_equirect.py
Surt: plantilles/graella_equirect_A4.svg, _A3.svg i, si troba Edge o Chrome, els PDF.
"""
import math
import shutil
import subprocess
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
SORTIDA = ARREL / "plantilles"

FORMATS = {
    # nom: (ample paper, alt paper, ample del marc) en mm; el marc fa sempre 2:1
    "A4": (297, 210, 262),
    "A3": (420, 297, 380),
}

GRIS = "#b9c3cf"
GRIS_FORT = "#8d9aa8"
HORITZO = "#5b8fd6"
GUIA = "#f4a261"

# Habitació de la guia: el visitant al centre, ulls a 1,6 m, parets a 3 m, sostre a 3 m
ULLS, PARET, SOSTRE = 1.6, 3.0, 3.0


def habitacio():
    """Polilínies (llistes de (longitud, latitud) en graus) de les arestes de l'habitació."""
    linies = []
    for paret in (0, 90, 180, 270):
        for alcada in (-ULLS, SOSTRE - ULLS):          # aresta amb el terra i amb el sostre
            punts = []
            for i in range(121):
                x = -PARET + 2 * PARET * i / 120
                lon = math.degrees(math.atan2(x, PARET)) + paret
                lat = math.degrees(math.atan2(alcada, math.hypot(x, PARET)))
                punts.append((((lon + 180) % 360) - 180, lat))
            # Talla la línia on salta de +180 a -180 (la paret de darrere)
            tram = [punts[0]]
            for a, b in zip(punts, punts[1:]):
                if abs(b[0] - a[0]) > 180:
                    linies.append(tram)
                    tram = []
                tram.append(b)
            linies.append(tram)
    racons = []
    for lon in (-135, -45, 45, 135):                     # racons verticals
        dist = PARET * math.sqrt(2)
        racons.append([(lon, math.degrees(math.atan2(-ULLS, dist))),
                       (lon, math.degrees(math.atan2(SOSTRE - ULLS, dist)))])
    return linies + racons


def svg(nom, paper_w, paper_h, marc_w):
    marc_h = marc_w / 2
    x0 = (paper_w - marc_w) / 2
    y0 = (paper_h - marc_h) / 2 + 3
    X = lambda lon: x0 + (lon + 180) / 360 * marc_w
    Y = lambda lat: y0 + (90 - lat) / 180 * marc_h
    mm = marc_w / 262                                   # escala de textos i gruixos

    s = []
    a = s.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{paper_w}mm" height="{paper_h}mm" '
      f'viewBox="0 0 {paper_w} {paper_h}" font-family="Arial, Helvetica, sans-serif">')
    a(f'<style>@page {{ size: {nom} landscape; margin: 0 }} body {{ margin: 0 }}</style>')
    a(f'<rect width="{paper_w}" height="{paper_h}" fill="#fff"/>')
    a('<defs><pattern id="ratlla" width="4" height="4" patternUnits="userSpaceOnUse" '
      'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="4" '
      f'stroke="{GRIS}" stroke-width="0.25"/></pattern></defs>')

    # Capçalera (fora del marc)
    a(f'<text x="{x0}" y="{y0 - 12 * mm}" font-size="{5.2 * mm}" font-weight="700">'
      'El nostre món en 360° — plantilla de dibuix</text>')
    a(f'<text x="{x0 + marc_w}" y="{y0 - 12 * mm}" font-size="{3.4 * mm}" text-anchor="end">'
      'Nom / equip: ______________________</text>')

    # Zones polars ratllades
    for lat_a, lat_b in ((90, 60), (-60, -90)):
        a(f'<rect x="{x0}" y="{Y(lat_a)}" width="{marc_w}" height="{Y(lat_b) - Y(lat_a)}" '
          'fill="url(#ratlla)"/>')

    # Graella
    for lon in range(-180, 181, 15):
        fort = lon % 45 == 0
        a(f'<line x1="{X(lon)}" y1="{y0}" x2="{X(lon)}" y2="{y0 + marc_h}" '
          f'stroke="{GRIS_FORT if fort else GRIS}" stroke-width="{(0.3 if fort else 0.15) * mm}"/>')
    for lat in range(-75, 90, 15):
        if lat == 0:
            continue
        fort = lat % 45 == 0
        a(f'<line x1="{x0}" y1="{Y(lat)}" x2="{x0 + marc_w}" y2="{Y(lat)}" '
          f'stroke="{GRIS_FORT if fort else GRIS}" stroke-width="{(0.3 if fort else 0.15) * mm}"/>')
    a(f'<line x1="{x0}" y1="{Y(0)}" x2="{x0 + marc_w}" y2="{Y(0)}" stroke="{HORITZO}" '
      f'stroke-width="{0.45 * mm}" stroke-dasharray="{3 * mm} {1.5 * mm}"/>')

    # Guia de l'habitació
    for linia in habitacio():
        punts = " ".join(f"{X(lo):.2f},{Y(la):.2f}" for lo, la in linia)
        a(f'<polyline points="{punts}" fill="none" stroke="{GUIA}" stroke-width="{0.35 * mm}" '
          f'stroke-dasharray="{1.6 * mm} {1.2 * mm}"/>')

    # Marc i marques de tall
    a(f'<rect x="{x0}" y="{y0}" width="{marc_w}" height="{marc_h}" fill="none" stroke="#000" '
      f'stroke-width="{0.5 * mm}"/>')
    t = 3 * mm
    for cx, cy, dx, dy in ((x0, y0, -1, -1), (x0 + marc_w, y0, 1, -1),
                           (x0, y0 + marc_h, -1, 1), (x0 + marc_w, y0 + marc_h, 1, 1)):
        a(f'<path d="M{cx + dx * 1.5} {cy} h{dx * t} M{cx} {cy + dy * 1.5} v{dy * t}" '
          f'stroke="#000" stroke-width="{0.25 * mm}"/>')

    # Etiquetes de direcció (a sota, fora del marc)
    direccions = {-180: "DARRERE", -90: "ESQUERRA", 0: "DAVANT", 90: "DRETA", 180: "DARRERE"}
    for lon in range(-180, 181, 45):
        a(f'<text x="{X(lon)}" y="{y0 + marc_h + 5 * mm}" font-size="{2.8 * mm}" '
          f'text-anchor="middle" fill="#555">{lon}°</text>')
        if lon in direccions:
            a(f'<text x="{X(lon)}" y="{y0 + marc_h + 9.5 * mm}" font-size="{3.4 * mm}" '
              f'font-weight="700" text-anchor="middle">{direccions[lon]}</text>')
    # Etiquetes d'altura (a l'esquerra, fora del marc)
    for lat in range(-90, 91, 45):
        txt = {90: "a sobre", 0: "horitzó", -90: "a sota"}.get(lat, f"{lat:+d}°")
        a(f'<text x="{x0 - 5 * mm}" y="{Y(lat) + 1 * mm}" font-size="{2.6 * mm}" '
          f'text-anchor="end" fill="#555">{txt}</text>')

    # Instruccions (peu)
    peu = y0 + marc_h + 16 * mm
    linies = [
        "1. Dibuixa dins el marc. El centre és el que veuràs DAVANT; les dues vores laterals són el mateix lloc (DARRERE) i s'han d'enganxar.",
        "2. Línia blava = horitzó, a l'alçada dels ulls. Les línies taronja són una habitació vista des del centre: les rectes surten corbades.",
        "3. Zones ratllades (dalt i baix): s'hi veu tot molt petit. Dibuixa-hi cel o terra, o coses ben amples. No hi posis el més important.",
        "4. Escaneja o fes una foto ben plana, retalla JUST pel marc negre i puja-la al constructor de mons com a «Imatge 360°».",
    ]
    for i, l in enumerate(linies):
        a(f'<text x="{x0}" y="{peu + i * 4.6 * mm}" font-size="{2.75 * mm}">{l}</text>')
    a("</svg>")
    return "\n".join(s)


def navegador():
    candidats = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidats:
        if Path(c).exists():
            return c
    return shutil.which("msedge") or shutil.which("chrome")


def main():
    SORTIDA.mkdir(exist_ok=True)
    nav = navegador()
    for nom, (w, h, marc) in FORMATS.items():
        fitxer = SORTIDA / f"graella_equirect_{nom}.svg"
        fitxer.write_text(svg(nom, w, h, marc), encoding="utf-8")
        print("SVG:", fitxer.relative_to(ARREL))
        if nav:
            # L'SVG s'imprimeix dins un HTML amb @page per fixar el paper apaïsat sense marges
            pdf = fitxer.with_suffix(".pdf")
            html = fitxer.with_suffix(".tmp")
            html.write_text(
                f'<!doctype html><meta charset="utf-8"><style>@page {{ size: {w}mm {h}mm; margin: 0 }}'
                f' html, body {{ margin: 0 }} svg {{ display: block }}</style>'
                + svg(nom, w, h, marc), encoding="utf-8")
            pagina = html.with_suffix(".html")
            html.replace(pagina)
            subprocess.run([nav, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={pdf}", pagina.as_uri()],
                           check=False, capture_output=True, timeout=60)
            pagina.unlink()
            print("PDF:" if pdf.exists() else "PDF no generat:", pdf.relative_to(ARREL))


if __name__ == "__main__":
    main()
