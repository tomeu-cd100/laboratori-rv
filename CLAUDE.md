# CLAUDE.md — Laboratori RV (Quest 3S + càmera 360)

Banc de proves del docent per preparar la **RV del 3r trimestre de 1r ESO**. **No és un curs**:
el material d'aula (SA7 tour 360, SA8 escenes VR, SA9 fira, protocol VR, autoritzacions) viu al
repo `Curs 2627 1 ESO Maker` i en continua sent la font única.

## Flux
1. Aquí es **prova** (eines, configuració de les ulleres, plantilles) i es documenta el
   resultat a `01_Registre_de_proves.md`.
2. Quan una prova canvia una decisió d'aula, s'aplica **al repo Maker** (SA7/SA8/SA9,
   `Normativa/Protocol_us_VR.md`) passant els seus verificadors i el skill **crear-sa**.
3. No dupliquis aquí seqüències, fitxes ni rúbriques del curs Maker.

## Context fix
- **5 Meta Quest 3S** (lents Fresnel, passthrough en color, ~2 h de bateria) + 1 càmera 360.
- Alumnat de 1r ESO (12 anys) amb **Chromebooks**: tot el que creïn ha de funcionar al
  navegador. Les Quest només visualitzen (navegador WebXR o apps validades).
- Política d'edat de Meta: es verifica i es documenta a la fitxa §8 del protocol (repo Maker).

## Regles
- Tot en català amb ortografia completa; identificadors de codi en la forma original.
- **RGPD**: cap foto 360 amb alumnat ni persones identificables al repo. Les fotos reals
  del centre van a `escenes_reals/` (gitignored) fins que s'hagin revisat.
- `formacio/` (transcripcions de reunions de la formació, amb terceres persones) és
  **gitignored**: mai es publica.
- Pàgines web sense build: HTML + A-Frame des de `https://aframe.io/releases/1.7.0/`.
  Textos dins l'escena 3D via `<canvas>` (les fonts MSDF d'A-Frame poden no tenir accents).
- Provar en local: `py -3.11 -m http.server 8931` (el port 8765 l'ocupa una altra app).
- `eines/genera_imatge_test.py` genera la imatge equirectangular de calibratge.
