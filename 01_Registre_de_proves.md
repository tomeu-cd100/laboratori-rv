# Registre de proves

> Cada prova respon una pregunta que **condiciona una decisió d'aula**. Quan tinguis el
> resultat, omple'l i aplica la decisió al repo Maker (columna «Afecta»).
> Estat: ⏳ pendent · ✅ funciona · ⚠️ funciona amb condicions · ❌ no funciona

| # | Pregunta | Com es prova | Estat | Resultat / notes | Afecta |
|---|----------|--------------|-------|------------------|--------|
| P1 | El visor de tour propi va al Chromebook i a les Quest? | `proves/visor-tour/` en local i publicat; mode VR i clic amb gallet | ⚠️ | Validat en navegador d'escriptori (orientació, punts, canvi d'escena). Falta provar a les Quest i al Chromebook. | SA7 (alternativa a CoSpaces sense comptes) |
| P2 | Com surten les fotos de la càmera 360 en JPG equirectangular 2:1? | Foto de prova → app de la càmera → exportar → obrir al visor | ⏳ | **Insta360** (model: ______). Els `.insp` són 2 fisheye sense unir: cal **exportar** a JPG equirectangular amb l'app mòbil Insta360 o Insta360 Studio (Windows/Mac, **no ChromeOS**) → qui exporta: docent o mòbil del centre? | SA7 S2 (flux de transferència) |
| P3 | Les fotos d'interior es veuen bé a les Quest 3S? | Foto real a `escenes_reals/` + visor | ⏳ | Resolució de la càmera, nitidesa, llum | SA7 criteris d'èxit (3 checks) |
| P4 | CoSpaces Edu: amb el **pla Basic** es pot veure una escena a les Quest 3S? Amb app o navegador? | Crear una escena de prova i obrir-la a les ulleres | ⏳ | | SA7 S3 / SA8 (Basic o Pro) |
| P5 | Marzipano Tool funciona al Chromebook i el resultat va a les Quest? | Tour de 2 escenes amb Marzipano → GitHub Pages | ⏳ | | SA7 alternativa |
| P6 | Un model de Tinkercad (.glb) es veu a escala real damunt la taula? | `proves/ra-taula/` amb el botó AR | ⏳ | Comprova que la mida (mm) coincideixi amb la de Tinkercad | ⭐ SA8 / SA9 (RA) |
| P7 | Es pot clicar el tour amb les mans (sense comandaments)? | P1 amb *hand tracking* | ⏳ | | SA7-SA8 (menys material a repartir) |
| P8 | El *casting* funciona a la Wi-Fi del centre? | `meta.com/casting` des d'un Chromebook | ⏳ | | SA7-SA8 (la resta del grup veu què passa) |
| P9 | Quines experiències de `Simulacions/Experiencies_VR_360.md` van a les 3S i són gratuïtes? | Instal·lar i provar 10' cadascuna | ⏳ | | SA8 S1 (estacions) |
| P10 | Quanta bateria gasten 2 h de classe amb 5 rondes? | Sessió simulada | ⏳ | | Logística |
| P11 | Política d'edat de Meta per a 12 anys | Termes vigents | ⏳ | Font i data: ______ | Protocol §8 (ulleres per a tothom o pantalla) |
| P12 | El constructor de mons va al Chromebook (editar, tancar, reobrir l'endemà) i el món es veu a les Quest? | `proves/constructor-mons/` publicat: món amb cel 360 + 2 models + rètol; mode VR, clic als objectes i al terra | ⚠️ | Validat en Chrome d'escriptori (2026-11-20): models normalitzats a 1 m sobre el terra, cel 360, missatges, desar/obrir .json, `?veure` i `?mon=`. Falta Chromebook i Quest. | SA8 opció B / SA9 (sense comptes) |
| P13 | Un `.glb` exportat de Tinkercad es veu bé al constructor (colors, mida, orientació)? | Exportar un disseny real de SA4-SA6 → afegir-lo al constructor | ⏳ | Provat només amb un cub sintètic en mm desplaçat de l'origen | SA9 (objecte fabricat dins el món) |
| P14 | Open Brush a les Quest 3S: es pot crear i exportar `.glb` sense compte, i treure el fitxer de les ulleres? | Instal·lar Open Brush, pintar, exportar, copiar per USB o Drive | ⏳ | | SA8 estació a les ulleres |
| P15 | Delightex (ex-CoSpaces) Basic: l'app de les Quest 3S obre un projecte? Quants projectes per alumne? | Classe de prova amb 2 alumnes fictius | ⏳ | Basic: 1 classe, 29 alumnes, 1 tasca, 2 projectes. Prova Pro: 14 dies, 24 alumnes | SA8 opció A |
| P16 | Un món complex (maqueta de la Seu, ~2.900 triangles, 9 models) va fluid a les Quest 3S i els missatges es llegeixen bé? | `?mon=mons/seu.json` a les ulleres: caminar al voltant, clicar les 7 esferes blaves | ⏳ | Comprovat amb un renderitzador propi (z-buffer + cel 360) des de 6 punts de vista; falta navegador real i Quest | SA8/SA9 (fins on poden complicar els mons) |
