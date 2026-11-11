# Laboratori RV — Quest 3S i càmera 360

Banc de proves per preparar la realitat virtual de **1r ESO (3r trimestre)**. El material
d'aula és al curs Maker 1r ESO (SA7 tour 360 · SA8 escenes VR · SA9 fira).

| Què | On |
|-----|----|
| Posar a punt les 5 ulleres | `00_Posada_en_marxa_Quest3S.md` |
| Proves pendents i resultats | `01_Registre_de_proves.md` |
| Visor de tour 360 (A-Frame, sense comptes) | `proves/visor-tour/` — s'edita només `tour.js`; amb `?editor` dona yaw/pitch en clicar |
| Model 3D damunt la taula (realitat mixta) | `proves/ra-taula/` — `?model=fitxer.glb` o botó «Obre un model» |
| Imatge de calibratge 360 | `py -3.11 eines/genera_imatge_test.py` |

**Provar en local:** `py -3.11 -m http.server 8931` i obre `http://127.0.0.1:8931/proves/visor-tour/`.
Per provar-ho a les Quest cal una URL https (GitHub Pages).
