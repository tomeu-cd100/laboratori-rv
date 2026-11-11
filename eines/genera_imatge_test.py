"""Genera una imatge equirectangular de prova (2:1) per calibrar visors 360.

Dibuixa una graella cada 30° (longitud) i cada 30° (latitud), la línia de l'horitzó i
etiquetes amb l'angle. Serveix per comprovar, en un visor (A-Frame, Marzipano, CoSpaces…),
on queda el centre de la imatge i si els punts del tour es col·loquen on toca.

Ús:  py -3.11 eines/genera_imatge_test.py [sortida.jpg]
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

AMPLE, ALT = 4096, 2048
SORTIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    Path(__file__).resolve().parent.parent / "proves" / "visor-tour" / "escenes" / "test.jpg"
)


def x_de_longitud(lon):
    """Longitud -180..180 (0 = centre de la imatge) → píxel x."""
    return (lon + 180) / 360 * AMPLE


def y_de_latitud(lat):
    """Latitud 90 (zenit) .. -90 (nadir) → píxel y."""
    return (90 - lat) / 180 * ALT


def main():
    img = Image.new("RGB", (AMPLE, ALT))
    d = ImageDraw.Draw(img)
    # Cel blau a dalt, terra marró a baix: així es veu de seguida si la imatge està capgirada.
    d.rectangle([0, 0, AMPLE, ALT // 2], fill=(70, 120, 190))
    d.rectangle([0, ALT // 2, AMPLE, ALT], fill=(120, 90, 60))

    gran = ImageFont.load_default(size=72)
    petit = ImageFont.load_default(size=40)

    for lon in range(-180, 181, 30):
        x = x_de_longitud(lon)
        d.line([(x, 0), (x, ALT)], fill=(255, 255, 255), width=3)
    for lat in range(-60, 61, 30):
        y = y_de_latitud(lat)
        d.line([(0, y), (AMPLE, y)], fill=(255, 255, 255), width=3)
        d.text((10, y + 6), f"{lat:+d}°", fill="white", font=petit)

    # Horitzó en vermell, més gruixut.
    d.line([(0, ALT / 2), (AMPLE, ALT / 2)], fill=(230, 40, 40), width=8)

    for lon in range(-150, 181, 30):
        d.text((x_de_longitud(lon) + 8, ALT / 2 + 10), f"{lon}°", fill="white", font=petit)

    rotuls = {0: "CENTRE (0°)", 90: "DRETA (90°)", -90: "ESQUERRA (-90°)", 180: "DARRERE"}
    for lon, text in rotuls.items():
        x = x_de_longitud(lon if lon != 180 else 179)
        caixa = d.textbbox((0, 0), text, font=gran)
        w = caixa[2] - caixa[0]
        x = min(max(x - w / 2, 10), AMPLE - w - 10)
        d.text((x, ALT / 2 - 140), text, fill=(255, 230, 0), font=gran)

    d.text((AMPLE / 2 - 200, 40), "ZENIT (amunt)", fill="white", font=gran)
    d.text((AMPLE / 2 - 200, ALT - 120), "NADIR (avall)", fill="white", font=gran)

    SORTIDA.parent.mkdir(parents=True, exist_ok=True)
    img.save(SORTIDA, quality=85)
    print(f"[OK] {SORTIDA} ({AMPLE}x{ALT})")


if __name__ == "__main__":
    main()
