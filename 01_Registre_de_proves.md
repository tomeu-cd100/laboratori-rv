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
