// ===================================================================
//  CONFIGURACIÓ DEL TOUR — l'únic fitxer que cal editar
// ===================================================================
//  - Cada escena és una foto 360 (equirectangular, proporció 2:1) dins `escenes/`.
//  - yaw   = angle horitzontal en graus (0 = davant, 90 = dreta, -90 = esquerra).
//  - pitch = angle vertical en graus (0 = horitzó, positiu = amunt).
//  - Per saber el yaw/pitch d'un lloc: obre la pàgina amb ?editor al final de l'adreça
//    i fes clic on vols el punt. Els valors surten a la part de baix de la pantalla.
//  - `gir` (opcional): gira tota la foto (graus) si l'escena no comença mirant on vols.
// ===================================================================

window.TOUR = {
  titol: "Tour de prova",
  inici: "entrada",

  escenes: {
    entrada: {
      titol: "Entrada (imatge de prova)",
      imatge: "escenes/test.jpg",
      gir: 0,
      punts: [
        { cap: "taller", yaw: 90, pitch: 0, etiqueta: "Cap al taller →" }
      ],
      info: [
        { yaw: 0, pitch: 20, text: "Això és el centre de la imatge (0°)." },
        { yaw: -90, pitch: 0, text: "Esquerra: −90°. Fes clic a la «i» per tancar." }
      ]
    },

    taller: {
      titol: "Taller (mateixa imatge, girada 90°)",
      imatge: "escenes/test.jpg",
      gir: 90,
      punts: [
        { cap: "entrada", yaw: -90, pitch: -10, etiqueta: "← Tornar a l'entrada" }
      ],
      info: []
    }
  }
};
