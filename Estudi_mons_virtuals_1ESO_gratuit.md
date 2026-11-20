# Estudi — Crear mons virtuals amb 1r d'ESO sense pagar

**Data:** 2026-11-20 · **Context:** Aula Maker 1r ESO, T3 (SA7 tour 360, SA8 escena VR, SA9 Fira) ·
**Material:** 5 Meta Quest 3S, càmera Insta360, Chromebooks

## Resposta curta

Es pot fer gratis si el món es munta **per capes**, i cada capa amb una eina gratuïta:

1. **Fons 360°:** una foto de la SA7 o un dibuix fet sobre una graella equirectangular.
2. **Objectes 3D:** dissenyats a Tinkercad, l'eina que ja fan servir a les SA4-SA6, i exportats en `.glb`.
3. **Visor web A-Frame del docent:** ajunta el fons, els objectes i els rètols, i s'obre al
   navegador de les Quest amb un QR.

L'alumnat no necessita cap compte nou. CoSpaces (ara **Delightex Edu**) queda com a opció per a la
SA8: es pot fer servir la **prova Pro de 14 dies**, activada just a les setmanes 29-30.

## El problema del pla actual

Ara mateix les SA7 i SA8 depenen de CoSpaces. El pla gratuït (Basic) es queda curt per a un grup
sencer:

| Pla Basic de Delightex (gratuït) | Límit |
|---|---|
| Alumnes | fins a 29, en 1 classe |
| Tasques | 1 |
| Projectes | 2 (la pàgina no aclareix si és per alumne o en total) |
| Biblioteca 3D | limitada |
| Programació | només CoBlocks bàsics, sense física ni scripts |
| Ulleres | es pot **explorar** en VR (app per a Meta), però no **crear** amb les ulleres |

El Pro costa 50 USD/any el primer seient i 7 USD/any cada seient més. La prova gratuïta dura
14 dies i té 25 seients: el docent i 24 alumnes.

**Comptes i edat:** l'alumnat de 1r d'ESO té 12-13 anys. Per sota dels 14 anys, el consentiment
per tractar dades el dona la família (LOPDGDD, art. 7). Cada eina que demana un compte personal
afegeix una autorització. Les opcions sense compte, o amb un compte per equip amb un àlies, eviten
aquest problema.

## Opcions estudiades

| Eina | On es crea | Es veu a les Quest? | Compte de l'alumnat | Cost | Encaix |
|---|---|---|---|---|---|
| **Visor A-Frame del docent** (com `visor-tour`) | Chromebook (formulari web) | Sí, navegador Quest (WebXR) | **No** | 0 € (GitHub Pages) | ⭐ Base de tot. Cal programar el constructor |
| **Tinkercad → `.glb`** | Chromebook | Sí, dins el visor A-Frame | El que ja tenen (codi de classe) | 0 € | ⭐ Reaprofita les SA4-SA6 |
| **Fons 360 dibuixat** (graella equirectangular, en paper o digital) | Paper o Chromebook | Sí, com a cel del visor | **No** | 0 € | ⭐ Molt maker, sense pantalla |
| **Fotos 360 de la SA7** (Insta360) | Càmera | Sí | **No** | 0 € | ⭐ Ja previst |
| **Delightex Edu Basic + prova Pro** | Chromebook (web) | Sí, app Delightex a Quest | Sí (codi de classe) | 0 € els 14 dies de prova | ✅ Per a la SA8, amb la data ben triada |
| **Open Brush** (pintar en 3D) | Dins les Quest | Sí (s'hi crea) | No per crear, sí per publicar | 0 €, codi obert | ✅ Estació de rotació amb 5 ulleres |
| **Open Blocks** (modelatge low-poly) | Dins les Quest | Sí | No per crear | 0 €, codi obert | ✅ Alternativa a Open Brush |
| Frame VR | Web | Sí | Convidat | Ara només té prova, no pla gratuït | ❌ |
| Minecraft Education | App | No a les Quest | Microsoft 365 | Llicència A3/A5 o de pagament | ❌ Llevat que el centre ja la tingui |
| Mozilla Hubs | — | — | — | Tancat el 2024 | ❌ |
| Spatial, Roblox, Horizon Worlds | — | — | Comptes per a +13 anys; Roblox Studio no funciona a Chromebook | — | ❌ |

## Proposta per a les SA7-SA9

| SA | Què fan | Eina | Comptes |
|---|---|---|---|
| **SA7** Tour 360 | Fotos 360 del centre amb punts per anar d'una a l'altra | Visor A-Frame (ja és al laboratori) en lloc de CoSpaces | Cap |
| **SA8** Escena VR | Escena interactiva per equips | **Opció A:** Delightex amb la prova Pro activada el primer dia de la setmana 29 (dura 14 dies; les 2 sessions hi caben). **Opció B:** el constructor A-Frame | A: 1 per equip, amb àlies. B: cap |
| **SA8** Estació a les ulleres | Mentre un equip construeix, un altre pinta a Open Brush (torns de 10') | Open Brush | Cap |
| **SA9** Fira | Món de l'estand: fons 360 + objectes fets a Tinkercad + rètols, i un QR a l'estand | Constructor A-Frame | Cap |

Fil de l'any: l'objecte que dissenyen a Tinkercad al T2 (SA4-SA6) es converteix en una peça del
seu món virtual al T3. Així es compleix el requisit de la SA9 de «combinar fabricació i
immersió» amb el mateix fitxer.

## Què caldria preparar

1. **Constructor de mons (web, al repo `laboratori-rv`):** l'alumnat tria un fons 360, puja
   1-3 `.glb` de Tinkercad, els col·loca i hi afegeix rètols. Es desa com a fitxer o enllaç, i
   es genera un QR per obrir-lo a les Quest. Funciona sense compte, i el docent publica els mons
   a GitHub Pages.
2. **Plantilla de graella equirectangular** (proporció 2:1) per dibuixar fons 360 en paper i
   escanejar-los.
3. **Proves a les ulleres** (afegir al `01_Registre_de_proves.md`):
   - Un `.glb` exportat de Tinkercad es veu bé al navegador de la Quest 3S (mida i colors).
   - Open Brush exporta en `.glb` sense compte i el fitxer surt de les ulleres.
   - L'app de Delightex a la Quest 3S obre un projecte del pla Basic.
   - Un fons dibuixat i escanejat es veu sense costures al visor.

## Fonts

- [Delightex — plans i preus](https://www.delightex.com/edu/pricing) i [FAQ](https://www.delightex.com/edu/tech-check-faq)
- [Frame VR — educació](https://learn.framevr.io/education)
- [Open Blocks a la Meta Store](https://www.meta.com/experiences/open-blocks-low-poly-3d-modelling/8043509915705378/) · [Open Blocks gratuït a Quest (Road to VR)](https://www.roadtovr.com/google-blocks-open-source-modeling-quest-3)
- [Open Brush 1.0, exportació glTF (Icosa)](https://opencollective.com/icosa/updates/2021-retrospective-and-open-brush-1-0) · [Exportació experimental](https://docs.openbrush.app/alternate-and-experimental-builds/improved-import-export)
- [A-Frame `gltf-model`](https://aframe.io/docs/1.6.0/components/gltf-model.html) · [Meta, WebXR first steps](https://developers.meta.com/horizon/documentation/web/webxr-first-steps-chapter4/)
- [Exportar de Tinkercad (Merge EDU)](https://support.mergeedu.com/hc/en-us/articles/360052931192-Exporting-Objects-from-Tinkercad)
