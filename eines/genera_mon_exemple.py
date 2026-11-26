"""Genera el món d'exemple «El rusc del Maker» per al constructor de mons.

Fa servir totes les peces del format `mon-v1`: cel 360 pintat (equirectangular 2:1),
dos models .glb (en mm i desplaçats de l'origen, com els exporta Tinkercad), formes,
rètols i missatges en clicar.

Sortides:
  proves/constructor-mons/mons/rusc.json        (món complet, amb tot incrustat)
  proves/constructor-mons/models/bresca.glb     (per provar «Afegeix model» a mà)
  proves/constructor-mons/models/rajola_hex.glb

Ús:  py -3.11 eines/genera_mon_exemple.py
"""
import base64
import io
import json
import math
import struct
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ARREL = Path(__file__).resolve().parent.parent / "proves" / "constructor-mons"
AMPLE, ALT = 4096, 2048
PRAT = (122, 176, 92)            # color del prat a l'horitzó = color del terra del món


# ---------------------------------------------------------------- cel 360
def pinta_cel():
    rng = np.random.default_rng(7)
    lon = np.linspace(-math.pi, math.pi, AMPLE, endpoint=False)          # columna → longitud
    lat = (0.5 - (np.arange(ALT) + 0.5) / ALT) * math.pi                  # fila → latitud
    LON, LAT = np.meshgrid(lon, lat)

    # Degradat del cel: blau intens a dalt, blau pàl·lid a l'horitzó
    t = np.clip(LAT / (math.pi / 2), 0, 1)[..., None]
    alt, baix = np.array([46, 110, 200]), np.array([196, 226, 250])
    img = baix + (alt - baix) * t ** 0.6

    # Sol amb halo (distància angular sobre l'esfera)
    sl, sb = math.radians(-35), math.radians(32)
    cosd = np.sin(LAT) * math.sin(sb) + np.cos(LAT) * math.cos(sb) * np.cos(LON - sl)
    d = np.arccos(np.clip(cosd, -1, 1))
    halo = np.exp(-(d / 0.35) ** 2)[..., None] * 0.55 + (d < 0.045)[..., None] * 1.0
    img = img + (np.array([255, 244, 214]) - img) * np.clip(halo, 0, 1)

    # Terra pintat sota l'horitzó (gairebé tapat pel pla del món, però evita un tall)
    terra = LAT < 0
    img[terra] = PRAT

    def serra(capes):
        """Perfil de muntanyes que tanca a ±180° (freqüències enteres)."""
        y = np.zeros_like(lon)
        for k, a, f in capes:
            y += a * np.sin(k * lon + f)
        return y

    # Muntanyes llunyanes (blavoses) i turons a prop (verds); alçada en graus
    for capes, base, color in (
        ([(2, 3.0, 0.4), (5, 1.6, 1.3), (11, 0.7, 2.0), (23, 0.3, 0.2)], 6.0, (128, 158, 186)),
        ([(3, 1.8, 2.2), (7, 1.0, 0.7), (13, 0.5, 1.1), (29, 0.2, 0.9)], 2.6, (98, 150, 80)),
    ):
        cim = np.radians(base + serra(capes))[None, :]
        dins = (LAT >= 0) & (LAT < cim)
        boira = np.clip(LAT / np.maximum(cim, 1e-3), 0, 1)[..., None]   # més clar al cim
        c = np.array(color) * (1 - 0.15 * boira) + 255 * 0.15 * boira
        img = np.where(dins[..., None], c, img)

    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

    # Núvols: el·lipses suaus i difuminades a la meitat de dalt
    nuv = Image.new("L", (AMPLE, ALT), 0)
    dib = ImageDraw.Draw(nuv)
    for _ in range(26):
        cx = rng.uniform(0, AMPLE)
        cy = rng.uniform(ALT * 0.18, ALT * 0.42)
        w = rng.uniform(140, 380) / max(math.cos((0.5 - cy / ALT) * math.pi), 0.3)
        for _ in range(5):
            dx, dy = rng.uniform(-w / 2, w / 2), rng.uniform(-30, 30)
            rx, ry = rng.uniform(w * 0.25, w * 0.5), rng.uniform(25, 55)
            for off in (-AMPLE, 0, AMPLE):                       # tanca la costura
                dib.ellipse((cx + dx - rx + off, cy + dy - ry, cx + dx + rx + off, cy + dy + ry), fill=210)
    nuv = nuv.filter(ImageFilter.GaussianBlur(18))
    im = Image.composite(Image.new("RGB", im.size, (252, 252, 255)), im, nuv)

    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------- .glb mínim
def prisma_hex(cx, cz, r_ext, r_int, y0, y1):
    """Triangles d'un prisma hexagonal (r_int=0) o d'un anell hexagonal. Vèrtex a 0°, 60°…"""
    ang = [math.radians(60 * i) for i in range(6)]
    ext = [(cx + r_ext * math.cos(a), cz + r_ext * math.sin(a)) for a in ang]
    tris = []
    for i in range(6):
        (ax, az), (bx, bz) = ext[i], ext[(i + 1) % 6]
        tris += [((ax, y0, az), (bx, y1, bz), (bx, y0, bz)), ((ax, y0, az), (ax, y1, az), (bx, y1, bz))]
        if r_int:
            ix, iz = cx + r_int * math.cos(ang[i]), cz + r_int * math.sin(ang[i])
            jx, jz = cx + r_int * math.cos(ang[(i + 1) % 6]), cz + r_int * math.sin(ang[(i + 1) % 6])
            tris += [((ix, y0, iz), (jx, y0, jz), (jx, y1, jz)), ((ix, y0, iz), (jx, y1, jz), (ix, y1, iz))]
            tris += [((ax, y1, az), (ix, y1, iz), (jx, y1, jz)), ((ax, y1, az), (jx, y1, jz), (bx, y1, bz))]
            tris += [((ax, y0, az), (jx, y0, jz), (ix, y0, iz)), ((ax, y0, az), (bx, y0, bz), (jx, y0, jz))]
        else:
            tris += [((cx, y1, cz), (bx, y1, bz), (ax, y1, az)), ((cx, y0, cz), (ax, y0, az), (bx, y0, bz))]
    return tris


def glb(parts):
    """parts: llista de (triangles, rgba). Normals planes, sense índexs."""
    binari, vistes, accessors, primitives, materials = b"", [], [], [], []
    for n, (tris, rgba) in enumerate(parts):
        pos, nor = [], []
        for a, b, c in tris:
            a, b, c = map(np.array, (a, b, c))
            nv = np.cross(b - a, c - a)
            nv = nv / (np.linalg.norm(nv) or 1)
            pos += [a, b, c]
            nor += [nv, nv, nv]
        pos, nor = np.array(pos, np.float32), np.array(nor, np.float32)
        for dades, extra in ((pos, {"min": pos.min(0).tolist(), "max": pos.max(0).tolist()}), (nor, {})):
            vistes.append({"buffer": 0, "byteOffset": len(binari), "byteLength": dades.nbytes, "target": 34962})
            accessors.append({"bufferView": len(vistes) - 1, "componentType": 5126,
                              "count": len(dades), "type": "VEC3", **extra})
            binari += dades.tobytes()
        materials.append({"pbrMetallicRoughness": {"baseColorFactor": rgba, "metallicFactor": 0,
                                                   "roughnessFactor": 0.8}, "doubleSided": True})
        primitives.append({"attributes": {"POSITION": 2 * n, "NORMAL": 2 * n + 1}, "material": n})
    doc = {"asset": {"version": "2.0", "generator": "genera_mon_exemple.py"},
           "scene": 0, "scenes": [{"nodes": [0]}], "nodes": [{"mesh": 0}],
           "meshes": [{"primitives": primitives}], "materials": materials,
           "buffers": [{"byteLength": len(binari)}], "bufferViews": vistes, "accessors": accessors}
    j = json.dumps(doc, separators=(",", ":")).encode()
    j += b" " * (-len(j) % 4)
    binari += b"\0" * (-len(binari) % 4)
    cos = struct.pack("<I4s", len(j), b"JSON") + j + struct.pack("<I4s", len(binari), b"BIN\0") + binari
    return struct.pack("<4sII", b"glTF", 2, 12 + len(cos)) + cos


def bresca():
    """7 cel·les hexagonals (mm), desplaçades de l'origen com un export de Tinkercad."""
    R, paret, h, base = 20.0, 2.0, 30.0, 3.0
    ox, oz = 60.0, 35.0
    centres = [(0, 0)] + [(math.sqrt(3) * R * math.cos(math.radians(30 + 60 * i)),
                           math.sqrt(3) * R * math.sin(math.radians(30 + 60 * i))) for i in range(6)]
    parets, fons = [], []
    for cx, cz in centres:
        parets += prisma_hex(cx + ox, cz + oz, R, R - paret / math.cos(math.radians(30)), 0, h)
        fons += prisma_hex(cx + ox, cz + oz, R, 0, 0, base)
    return glb([(parets, [0.96, 0.71, 0.05, 1]), (fons, [0.72, 0.42, 0.05, 1])])


def rajola():
    """Rajola hexagonal de la SA3: 115,5 mm entre vèrtexs (100 mm entre costats), 3 mm de gruix."""
    exterior = prisma_hex(80, 80, 57.75, 0, 0, 3)
    sanefa = prisma_hex(80, 80, 45, 41, 3, 5)
    return glb([(exterior, [0.93, 0.89, 0.80, 1]), (sanefa, [0.80, 0.33, 0.20, 1])])


def data_glb(b):
    return "data:model/gltf-binary;base64," + base64.b64encode(b).decode()


# ---------------------------------------------------------------- món
def obj(id_, tipus, nom, x, y, z, mida, color="#e76f51", text="", missatge="", gir=0, **extra):
    return {"id": id_, "tipus": tipus, "nom": nom, "color": color, "text": text, "missatge": missatge,
            "x": x, "y": y, "z": z, "girY": gir, "mida": mida, **extra}


def main():
    b_bresca, b_rajola = bresca(), rajola()
    (ARREL / "models").mkdir(exist_ok=True)
    (ARREL / "models" / "bresca.glb").write_bytes(b_bresca)
    (ARREL / "models" / "rajola_hex.glb").write_bytes(b_rajola)

    flors = []
    for i, (x, z, c) in enumerate([(-4.6, -1.2, "#e63946"), (-5.3, 0.2, "#9b5de5"), (-4.4, 1.3, "#f15bb5"),
                                   (-3.6, -2.4, "#fee440")]):
        flors += [obj(f"f{i}t", "con", f"Flor {i + 1} (fulles)", x, 0, z, 0.5, "#3a8d3f"),
                  obj(f"f{i}c", "esfera", f"Flor {i + 1}", x, 0.42, z, 0.32, c,
                      missatge="Les abelles recullen nèctar\ni pol·len de les flors." if i == 0 else "")]

    mon = {
        "format": "mon-v1",
        "titol": "El rusc del Maker",
        "cel": {"tipus": "imatge", "color": "#9ad0ff", "imatge": pinta_cel(), "gir": 0},
        "terra": {"visible": True, "color": "#%02x%02x%02x" % PRAT},
        "objectes": [
            obj("benvinguda", "text", "Benvinguda", 0, 1.0, -6.5, 2.8, "#e76f51",
                text="Benvinguts al Rusc del Maker!\nClica els objectes per saber-ne més.\n"
                     "Clica el terra per caminar."),
            obj("bresca", "model", "Bresca", -2.2, 0, -4, 1.3, gir=15, model=data_glb(b_bresca),
                missatge="Una bresca: cel·les hexagonals.\nAmb la mateixa cera, l'hexàgon\n"
                         "tanca més espai que el quadrat\no el triangle."),
            obj("abella", "esfera", "Abella", -1.4, 1.5, -3.6, 0.3, "#ffc300",
                missatge="Bzzz! Sóc una abella.\nPuc volar uns quants quilòmetres\nper trobar flors."),
            obj("abella-cap", "esfera", "Cap de l'abella", -1.22, 1.58, -3.5, 0.16, "#222222"),
            obj("pedestal", "cilindre", "Pedestal", 2.2, 0, -4, 0.9, "#d8d3c4"),
            obj("rajola", "model", "Rajola hexagonal", 2.2, 0.9, -4, 0.75, gir=10, model=data_glb(b_rajola),
                missatge="La rajola hexagonal de la SA3:\n115,5 × 100 mm, tallada amb làser.\n"
                         "Aquí la veus 6 vegades més gran."),
            obj("rusc", "cub", "Rusc de fusta", 5.2, 0, 0.5, 1.2, "#d9a441", gir=-30,
                missatge="Un rusc de fusta.\nA dins hi poden viure\nfins a 50.000 abelles."),
            obj("teulada", "con", "Teulada del rusc", 5.2, 1.2, 0.5, 1.5, "#8d5524"),
            obj("arbre1-tronc", "cilindre", "Tronc 1", -2.5, 0, 5.5, 0.45, "#7a4e2d"),
            obj("arbre1-copa", "esfera", "Copa 1", -2.5, 0.45, 5.5, 1.8, "#2a9d55"),
            obj("arbre2-tronc", "cilindre", "Tronc 2", 2.8, 0, 6.5, 0.5, "#7a4e2d"),
            obj("arbre2-copa", "esfera", "Copa 2", 2.8, 0.5, 6.5, 2.2, "#228b4c",
                missatge="Els arbres també floreixen:\nel til·ler i el castanyer\nagraden molt a les abelles."),
            obj("credits", "text", "Com s'ha fet", 0, 1.0, 4.2, 2.4, gir=180,
                text="Has mirat enrere!\nAquest món té: un cel 360, 2 models .glb\n"
                     "de Tinkercad, formes, rètols i missatges."),
            *flors,
        ],
    }
    sortida = ARREL / "mons" / "rusc.json"
    sortida.write_text(json.dumps(mon, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{sortida}  {sortida.stat().st_size / 1024:.0f} KB · {len(mon['objectes'])} objectes")


if __name__ == "__main__":
    main()
