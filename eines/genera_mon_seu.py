"""Genera el món «La Seu de Mallorca» (maqueta gegant) per al constructor de mons.

Models generats per codi (com si fossin de Tinkercad): la catedral damunt la murada, el llac
del Parc de la Mar i una palmera. Cel 360 amb la mar al darrere i la Tramuntana al davant.
Punts d'informació (esferes blaves) amb missatges.

Mides aproximades de la catedral (m): ~117 de llarg, nau central de 44 d'alt, rosassa major
de gairebé 14 de diàmetre. És una maqueta simplificada, no un model fidel.

Sortides:
  proves/constructor-mons/mons/seu.json
  proves/constructor-mons/models/seu.glb · llac.glb · palmera.glb

Ús:  py -3.11 eines/genera_mon_seu.py
"""
import base64
import io
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from genera_mon_exemple import glb, obj

ARREL = Path(__file__).resolve().parent.parent / "proves" / "constructor-mons"
AMPLE, ALT = 4096, 2048
PAVIMENT = "#cdbf9f"


def lin(hexa, a=1.0):
    """Color sRGB (#rrggbb) → factor lineal de glTF."""
    c = [int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return [round(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92, 4) for v in c] + [a]


# ---------------------------------------------------------------- primitives geomètriques
def quad(a, b, c, d):
    return [(a, b, c), (a, c, d)]


def bloc(c):
    """Sòlid de 6 cares a partir de c(i, j, k) amb i, j, k ∈ {0, 1} (pot ser inclinat)."""
    t = []
    for eix in range(3):
        for v in (0, 1):
            def p(u, w):
                idx = [0, 0, 0]
                idx[eix] = v
                idx[(eix + 1) % 3], idx[(eix + 2) % 3] = u, w
                return c(*idx)
            t += quad(p(0, 0), p(1, 0), p(1, 1), p(0, 1))
    return t


def caixa(x0, x1, y0, y1, z0, z1):
    return bloc(lambda i, j, k: ((x0, x1)[i], (y0, y1)[j], (z0, z1)[k]))


def biga(p0, p1, mx, mh):
    """Biga inclinada (arcbotant) de p0 a p1 en el pla y-z, amplada 2·mx en x."""
    def c(i, j, k):
        p = (p0, p1)[k]
        return (p[0] + (-mx, mx)[i], p[1] + (-mh, mh)[j], p[2])
    return bloc(c)


def prisma(cx, cz, r, n, y0, y1, gir=0.0, r_dalt=None):
    """Prisma (o tronc de piràmide si r_dalt) de n costats."""
    r_dalt = r if r_dalt is None else r_dalt
    angs = [gir + 2 * math.pi * i / n for i in range(n)]
    baix = [(cx + r * math.cos(a), y0, cz + r * math.sin(a)) for a in angs]
    dalt = [(cx + r_dalt * math.cos(a), y1, cz + r_dalt * math.sin(a)) for a in angs]
    t = []
    for i in range(n):
        j = (i + 1) % n
        t += quad(baix[i], baix[j], dalt[j], dalt[i])
        t.append(((cx, y0, cz), baix[j], baix[i]))
        if r_dalt > 0:
            t.append(((cx, y1, cz), dalt[i], dalt[j]))
    return t


def piramide(cx, cz, r, n, y0, y1, gir=math.pi / 4):
    return prisma(cx, cz, r, n, y0, y1, gir, r_dalt=0)


def pinacle(cx, cz, y0, costat=1.2, alt=3.0, punta=4.0):
    r = costat / math.sqrt(2)
    return prisma(cx, cz, r, 4, y0, y0 + alt, math.pi / 4) + piramide(cx, cz, r * 1.05, 4, y0 + alt, y0 + alt + punta)


def pla(punts):
    """Polígon pla convex (ventall des del primer punt)."""
    return [(punts[0], punts[i], punts[i + 1]) for i in range(1, len(punts) - 1)]


def ogiva(eix, pos, centre, y0, y1, ample, s=0.15):
    """Finestra o portal apuntat (rectangle + punta) sobre una paret.
    eix='z': paret perpendicular a z a z=pos (centre = x); eix='x': paret a x=pos (centre = z)."""
    h_punta = ample * 0.8
    perfil = [(-ample / 2, y0), (ample / 2, y0), (ample / 2, y1 - h_punta), (0, y1), (-ample / 2, y1 - h_punta)]
    if eix == "z":
        return pla([(centre + u, v, pos + s) for u, v in perfil])
    return pla([(pos + s, v, centre + u) for u, v in perfil])


def rosassa(eix, pos, centre, cy, r, colors, s=0.2):
    """Disc de vitralls: centre + 2 anells de sectors de colors alterns. Retorna {color: triangles}."""
    def p(u, v):
        return (centre + u, cy + v, pos + s) if eix == "z" else (pos + s, cy + v, centre + u)
    sortida = {c: [] for c in colors}
    n = 16
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        for anell, (ri, re) in enumerate(((0.3 * r, 0.7 * r), (0.7 * r, r))):
            col = colors[1 + (i + anell) % (len(colors) - 1)]
            sortida[col] += quad(p(ri * math.cos(a0), ri * math.sin(a0)), p(re * math.cos(a0), re * math.sin(a0)),
                                 p(re * math.cos(a1), re * math.sin(a1)), p(ri * math.cos(a1), ri * math.sin(a1)))
        sortida[colors[0]].append((p(0, 0), p(0.3 * r * math.cos(a0), 0.3 * r * math.sin(a0)),
                                   p(0.3 * r * math.cos(a1), 0.3 * r * math.sin(a1))))
    return sortida


# ---------------------------------------------------------------- la Seu
# Eixos del model: x = oest (−) → est (+), y = amunt, z = nord (−) → sud (+), en metres.
F = 6.0                                   # alçada del terrat de la murada (terra de la catedral)
X_OEST, X_EST = -55.0, 40.0               # nau: façana principal (oest) i mur de la rosassa (est)
CONTRAFORTS = np.linspace(-47, 33, 8)


def seu():
    pedra, fosca, murada, vidre, porta = [], [], [], [], []
    vitralls = {"#f1d27a": [], "#c0392b": [], "#2e5fb8": [], "#e9a23b": []}

    # Murada (Dalt Murada) amb ampit
    murada += caixa(-58, 68, 0, F, -42, 36)
    murada += caixa(-58, 68, F, F + 1.2, 35, 36)

    # Naus: central (44 m), laterals (30 m) i capelles entre contraforts (20 m)
    pedra += caixa(X_OEST, X_EST, F, F + 44, -10, 10)
    for sg in (-1, 1):
        pedra += caixa(X_OEST, X_EST, F, F + 30, *sorted((sg * 10, sg * 19)))
        pedra += caixa(X_OEST + 3, X_EST - 3, F, F + 20, *sorted((sg * 19, sg * 26)))

    # Capçalera esglaonada: capella reial i capella de la Trinitat
    pedra += caixa(X_EST, 54, F, F + 28, -10, 10)
    pedra += caixa(54, 61, F, F + 20, -6, 6)
    for z in (-6, 6):
        fosca += pinacle(54, z, F + 28, 1.4, 3, 4)

    # Contraforts amb pinacles i arcbotants, als dos costats
    for x in CONTRAFORTS:
        for sg in (-1, 1):
            z_in, z_out = sg * 19, sg * 27.5
            fosca += caixa(x - 1.1, x + 1.1, F, F + 34, *sorted((z_in, z_out)))
            fosca += pinacle(x, sg * 24.5, F + 34, 1.5, 3.5, 5)
            fosca += biga((x, F + 31.5, sg * 21.5), (x, F + 40.5, sg * 10.2), 0.6, 0.8)
            fosca += pinacle(x, sg * 10.5, F + 44, 1.0, 2.0, 3)      # pinacles de la nau central
            fosca += pinacle(x, sg * 18.5, F + 30, 0.9, 1.8, 2.5)    # pinacles de les naus laterals
        # Finestrals entre contraforts (només si hi cap la bahia)
        if x < CONTRAFORTS[-1]:
            xm = x + (CONTRAFORTS[1] - CONTRAFORTS[0]) / 2
            for sg in (-1, 1):
                vidre += ogiva("z", sg * 10, xm, F + 32, F + 42, 4.5, s=sg * 0.15)
                vidre += ogiva("z", sg * 19, xm, F + 21, F + 28.5, 4.0, s=sg * 0.15)
                vidre += ogiva("z", sg * 26, xm, F + 7, F + 17, 3.0, s=sg * 0.15)

    # Façana principal (oest): torretes octogonals, portal major, rosassa petita
    for z in (-11.5, 11.5):
        pedra += prisma(X_OEST - 1, z, 3.2, 8, F, F + 48, math.pi / 8)
        fosca += piramide(X_OEST - 1, z, 3.4, 8, F + 48, F + 58, math.pi / 8)
    porta += ogiva("x", X_OEST, 0, F, F + 16, 8, s=-0.15)
    fosca += pla([(X_OEST - 0.3, F + 17, -6), (X_OEST - 0.3, F + 17, 6), (X_OEST - 0.3, F + 25, 0)])
    for col, tris in rosassa("x", X_OEST, 0, F + 33, 4.0, list(vitralls), s=-0.2).items():
        vitralls[col] += tris

    # Rosassa major, al mur est de la nau central (sobre la capella reial)
    for col, tris in rosassa("x", X_EST, 0, F + 36.5, 6.9, list(vitralls), s=0.2).items():
        vitralls[col] += tris

    # Portal del Mirador (sud): porxo amb frontó, mirant a la mar
    pedra += caixa(4, 16, F, F + 18, 26, 29)
    fosca += pla([(4, F + 18, 29.05), (16, F + 18, 29.05), (10, F + 25, 29.05)])
    porta += ogiva("z", 29, 10, F, F + 13, 6, s=0.15)
    fosca += pinacle(4, 28, F + 18, 1.0, 2, 3) + pinacle(16, 28, F + 18, 1.0, 2, 3)

    # Campanar (nord), quadrat i massís
    pedra += caixa(-24, -14, F, F + 47, -37, -27)
    fosca += caixa(-24.6, -13.4, F + 45, F + 48, -37.6, -26.4)
    for xs in (-21, -17):
        vidre += ogiva("z", -27, xs, F + 34, F + 42, 2.0, s=0.15)

    parts = [(pedra, lin("#dcbc80")), (fosca, lin("#c9a466")), (murada, lin("#b89f74")),
             (vidre, lin("#2c3550")), (porta, lin("#4a3725"))]
    parts += [(t, lin(c)) for c, t in vitralls.items()]
    return glb(parts), (pedra + fosca + murada)


def llac():
    """Llac allargat (rectangle amb extrems arrodonits) amb vora de pedra baixa."""
    def contorn(rx, rz, n=40):
        pts = []
        for i in range(n):
            a = 2 * math.pi * i / n
            ca, sa = math.cos(a), math.sin(a)
            pts.append((rx * np.sign(ca) * abs(ca) ** 0.35, rz * np.sign(sa) * abs(sa) ** 0.35))
        return pts
    ext, inn = contorn(50, 12), contorn(47, 10)
    vora = []
    for i in range(len(ext)):
        j = (i + 1) % len(ext)
        (ax, az), (bx, bz), (cx_, cz_), (dx, dz) = ext[i], ext[j], inn[j], inn[i]
        vora += quad((ax, 1.2, az), (bx, 1.2, bz), (cx_, 1.2, cz_), (dx, 1.2, dz))
        vora += quad((ax, 0, az), (bx, 0, bz), (bx, 1.2, bz), (ax, 1.2, az))
    aigua = pla([(x, 0.6, z) for x, z in inn])
    return glb([(vora, lin("#c8b994")), (aigua, lin("#3f8fb5"))])


def palmera():
    tronc, fulles = [], []
    segs, h = 8, 12.0
    for i in range(segs):
        y0, y1 = h * i / segs, h * (i + 1) / segs
        dx0, dx1 = 0.8 * (y0 / h) ** 2, 0.8 * (y1 / h) ** 2           # lleugerament inclinada
        r = 0.35 - 0.1 * i / segs
        t = prisma(dx0, 0, r, 6, y0, y1)
        tronc += [tuple((p[0] + (dx1 - dx0) * (p[1] - y0) / (y1 - y0), p[1], p[2]) for p in tri) for tri in t]
    top = (0.8, h, 0.0)
    perfil = [(0, 0, 0.15), (1.6, 0.7, 0.55), (3.2, 0.4, 0.45), (4.6, -0.9, 0.05)]   # (dist, alçada, mitja amplada)
    for k in range(9):
        a = 2 * math.pi * k / 9 + 0.3
        ux, uz = math.cos(a), math.sin(a)
        px, pz = -uz, ux
        for (d0, h0, w0), (d1, h1, w1) in zip(perfil, perfil[1:]):
            p = lambda d, hh, w: (top[0] + ux * d + px * w, top[1] + hh, top[2] + uz * d + pz * w)
            fulles += quad(p(d0, h0, -w0), p(d1, h1, -w1), p(d1, h1, w1), p(d0, h0, w0))
    return glb([(tronc, lin("#8a6a45")), (fulles, lin("#3f8f3a"))])


# ---------------------------------------------------------------- cel 360
def pinta_cel():
    rng = np.random.default_rng(1229)
    lon = np.linspace(-math.pi, math.pi, AMPLE, endpoint=False)          # 0 = davant (cap a la Seu)
    lat = (0.5 - (np.arange(ALT) + 0.5) / ALT) * math.pi
    LON, LAT = np.meshgrid(lon, lat)
    t = np.clip(LAT / (math.pi / 2), 0, 1)[..., None]
    img = np.array([200, 226, 245]) + (np.array([40, 105, 190]) - np.array([200, 226, 245])) * t ** 0.55

    sl, sb = math.radians(140), math.radians(28)                           # sol damunt la mar, a la dreta
    d = np.arccos(np.clip(np.sin(LAT) * math.sin(sb) + np.cos(LAT) * math.cos(sb) * np.cos(LON - sl), -1, 1))
    img = img + (np.array([255, 245, 220]) - img) * np.clip(np.exp(-(d / 0.3) ** 2)[..., None] * 0.6 + (d < 0.04)[..., None], 0, 1)

    # Pes «terra» (davant) ↔ «mar» (darrere), suau i tancat a ±180°
    terra = np.clip((np.cos(lon) + 0.15) / 0.5, 0, 1)                    # 1 davant, 0 darrere

    def serra(capes, base):
        y = np.full_like(lon, base)
        for k, a, f in capes:
            y += a * np.sin(k * lon + f)
        return y

    muntanya = np.radians(serra([(2, 1.5, 0.3), (4, 1.2, 1.9), (9, 0.6, 0.4), (19, 0.25, 2.2)], 3.2) * terra)[None, :]
    dins = (LAT >= 0) & (LAT < muntanya)
    img = np.where(dins[..., None], np.array([118, 140, 150]), img)

    # Ciutat: blocs baixos de color marès just damunt l'horitzó
    alt_ciutat = np.zeros_like(lon)
    x = 0
    while x < AMPLE:
        w = int(rng.integers(12, 40))
        alt_ciutat[x:x + w] = rng.uniform(0.3, 1.1)
        x += w
    ciutat = np.radians(alt_ciutat * terra)[None, :]
    dins = (LAT >= 0) & (LAT < ciutat)
    to_ciutat = np.array([224, 205, 170]) * (0.9 + 0.1 * np.sin(np.arange(AMPLE) * 0.7))[None, :, None]
    img = np.where(dins[..., None], to_ciutat, img)

    # Sota l'horitzó: mar al darrere, paviment al davant
    sota = LAT < 0
    mar = np.array([31, 96, 150]) + (np.array([70, 140, 185]) - np.array([31, 96, 150])) * np.clip(-LAT / 0.08, 0, 1)[..., None]
    pav = np.array([int(PAVIMENT[i:i + 2], 16) for i in (1, 3, 5)])
    tw = terra[None, :, None]
    img = np.where(sota[..., None], pav * tw + mar * (1 - tw), img)

    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    dib = ImageDraw.Draw(im)
    y_hor = ALT / 2
    # Velers a la mar (darrere)
    for lon_v in (150, 172, -160, -128, 120):
        x = (lon_v + 180) / 360 * AMPLE
        dib.polygon([(x, y_hor - 2), (x + 10, y_hor - 2), (x + 3, y_hor - 30)], fill=(250, 250, 250))
        dib.rectangle((x - 6, y_hor - 2, x + 14, y_hor + 2), fill=(90, 70, 60))

    nuv = Image.new("L", im.size, 0)
    dn = ImageDraw.Draw(nuv)
    for _ in range(18):
        cx, cy = rng.uniform(0, AMPLE), rng.uniform(ALT * 0.2, ALT * 0.44)
        w = rng.uniform(150, 360)
        for _ in range(5):
            dx, dy = rng.uniform(-w / 2, w / 2), rng.uniform(-25, 25)
            rx, ry = rng.uniform(w * 0.25, w * 0.5), rng.uniform(20, 45)
            for off in (-AMPLE, 0, AMPLE):
                dn.ellipse((cx + dx - rx + off, cy + dy - ry, cx + dx + rx + off, cy + dy + ry), fill=190)
    nuv = nuv.filter(ImageFilter.GaussianBlur(18))
    im = Image.composite(Image.new("RGB", im.size, (252, 252, 255)), im, nuv)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------- món
def data_glb(b):
    return "data:model/gltf-binary;base64," + base64.b64encode(b).decode()


def main():
    b_seu, tris = seu()
    b_llac, b_palmera = llac(), palmera()
    for nom, b in (("seu", b_seu), ("llac", b_llac), ("palmera", b_palmera)):
        (ARREL / "models" / f"{nom}.glb").write_bytes(b)

    # Mateixa normalització que el constructor: centre en x/z, base a y=0, costat més llarg = mida
    pts = np.array([p for t in tris for p in t])
    mn, mx = pts.min(0), pts.max(0)
    MIDA, POS = 10.0, (0.0, 0.0, -12.5)
    s = MIDA / (mx - mn).max()
    cx, cz = (mn[0] + mx[0]) / 2, (mn[2] + mx[2]) / 2

    def mon_de(x, y, z):
        """Punt del model de la Seu (m reals) → posició al món (m de la maqueta)."""
        return round(POS[0] + (x - cx) * s, 2), round((y - mn[1]) * s, 2), round(POS[2] + (z - cz) * s, 2)

    def info(id_, nom, punt, missatge):
        x, y, z = mon_de(*punt)
        return obj(id_, "esfera", nom, x, y, z, 0.28, "#3a86ff", missatge=missatge)

    z_murada_sud = mon_de(0, 0, 36)[2]
    palmeres = []
    for i, x in enumerate((-5.5, -2.0, 2.0, 5.5, -6.8, 6.8)):
        z = z_murada_sud + (0.5 if i < 4 else 2.0)
        palmeres.append(obj(f"palmera{i}", "model", f"Palmera {i + 1}", x, 0, z, 0.95 + 0.08 * (i % 3),
                            gir=37 * i, model=data_glb(b_palmera)))
    palmeres[0]["missatge"] = "Les palmeres del Parc de la Mar.\nA aquesta escala, una palmera\nde 12 m fa menys d'1 m."

    mon = {
        "format": "mon-v1",
        "titol": "La Seu de Mallorca",
        "cel": {"tipus": "imatge", "color": "#9ad0ff", "imatge": pinta_cel(), "gir": 0},
        "terra": {"visible": True, "color": PAVIMENT},
        "objectes": [
            obj("seu", "model", "La Seu", *POS, MIDA, model=data_glb(b_seu),
                missatge="La Seu de Mallorca, catedral gòtica\nde pedra de marès, damunt la murada.\n"
                         "Aquesta maqueta és unes 13 vegades\nmés petita que la de veritat."),
            obj("llac", "model", "Llac del Parc de la Mar", 0, 0, z_murada_sud + 2.3, 9.0, model=data_glb(b_llac),
                missatge="El llac del Parc de la Mar:\nquan no fa vent, s'hi reflecteix la Seu."),
            *palmeres,
            obj("titol", "text", "Benvinguda", -3.8, 1.0, -2.9, 2.0, gir=50,
                text="La Seu de Mallorca\nMaqueta gegant (escala ≈ 1:13)\n"
                     "Clica les esferes blaves\nper descobrir-ne els secrets."),
            obj("mar", "text", "La mar", 0, 1.2, 4.0, 2.4, gir=180,
                text="Darrere teu, la mar Mediterrània.\nLa Seu mira a la badia de Palma."),
            info("i-contraforts", "Info: contraforts", (CONTRAFORTS[2], F + 30, 31),
                 "Contraforts i arcbotants:\naguanten l'empenta de les voltes.\n"
                 "Així les parets poden tenir\nfinestrals grans i molta llum."),
            info("i-nau", "Info: nau central", (CONTRAFORTS[4], F + 47, 12),
                 "La nau central fa 44 m d'alt:\nés una de les més altes\nde totes les catedrals gòtiques."),
            info("i-rosassa", "Info: rosassa major", (X_EST + 3, F + 36.5, 9),
                 "La rosassa major fa gairebé 14 m\nde diàmetre: una de les més grans\ndel gòtic."),
            info("i-llum", "Info: Festa de la Llum", (X_OEST - 4, F + 33, 8),
                 "Festa de la Llum (2 de febrer i 11 de novembre):\nel sol del matí travessa la rosassa major\n"
                 "i en projecta els colors davall\nd'aquesta rosassa, la de l'altra banda."),
            info("i-historia", "Info: història", (10, F + 27, 31),
                 "Jaume I la va prometre en conquerir\nMallorca (1229). Les obres van durar\n"
                 "segles: es va consagrar el 1601."),
            info("i-gaudi", "Info: Gaudí", ((CONTRAFORTS[5] + CONTRAFORTS[6]) / 2, F + 12, 31),
                 "Entre 1904 i 1914, Antoni Gaudí\nva reformar l'interior: va treure el cor\n"
                 "del mig de la nau i hi va posar\nun baldaquí de ferro i llums."),
            info("i-campanar", "Info: campanar", (-19, F + 50, -27),
                 "El campanar, a la banda nord:\nuna torre quadrada i massissa\nque s'acaba amb un terrat."),
        ],
    }
    sortida = ARREL / "mons" / "seu.json"
    sortida.write_text(json.dumps(mon, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{sortida}  {sortida.stat().st_size / 1024:.0f} KB · {len(mon['objectes'])} objectes · "
          f"escala 1:{1 / s:.1f} · nau {44 * s:.2f} m d'alt a la maqueta")


if __name__ == "__main__":
    main()
