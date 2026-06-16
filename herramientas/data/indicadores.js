/*
  INDICADORES PREVISIONALES Y TRIBUTARIOS — CHILE
  Fuente única de verdad para todas las herramientas de mistercontador.cl
  Última revisión: 2026-06-16
  Próxima revisión obligatoria: enero 2027 (reajuste anual de topes UF y UTM/UTA)
*/

window.MC_INDICADORES = {
  vigenciaDesde: '2026-01-01',
  ultimaRevision: '2026-06-16',

  // ── Sueldo mínimo mensual (IMM) ─────────────────────────────────────────
  // Ley 21.751 (vigente desde mayo 2026)
  sueldoMinimo: 529000,

  // ── Topes imponibles (en UF, valor enero 2026) ──────────────────────────
  // Convertir a CLP multiplicando por UF del día.
  topeAFP_UF: 87.8,        // tope cotización AFP y salud
  topeAFC_UF: 131.8,       // tope cotización Seguro de Cesantía (AFC)
  topeIPS_UF: 60.0,        // tope para regímenes IPS antiguos (referencial)

  // ── Cotización obligatoria AFP ──────────────────────────────────────────
  cotizacionAFP: 0.10,     // 10% obligatorio sobre renta imponible
  cotizacionSalud: 0.07,   // 7% legal (Fonasa o tramo mínimo Isapre)

  // ── Comisiones AFP (vigentes a junio 2026, sobre renta imponible) ────────
  comisionesAFP: {
    capital:   0.0144,
    cuprum:    0.0144,
    habitat:   0.0127,
    modelo:    0.0058,
    planvital: 0.0116,
    provida:   0.0145,
    uno:       0.0049,
    estimada:  0.0127   // fallback cuando el usuario no la conoce
  },

  // ── Seguro de Cesantía (AFC) ────────────────────────────────────────────
  // Trabajador SOLO paga si tiene contrato indefinido (0,6%).
  // Plazo fijo / obra: 0% trabajador, 3% empleador.
  AFC: {
    indefinido: { trabajador: 0.006, empleador: 0.024 },
    plazoFijo:  { trabajador: 0.000, empleador: 0.030 }
  },

  // ── Tramos Impuesto Único de 2ª Categoría (IUSC) ────────────────────────
  // Valores expresados en UTM mensuales. Cantidad a rebajar también en UTM.
  // Fuente: SII (tabla mensual vigente 2026).
  tramosIUSC: [
    { desde:   0.0, hasta:  13.5, factor: 0.000, rebajaUTM:  0.00 },
    { desde:  13.5, hasta:  30.0, factor: 0.040, rebajaUTM:  0.54 },
    { desde:  30.0, hasta:  50.0, factor: 0.080, rebajaUTM:  1.74 },
    { desde:  50.0, hasta:  70.0, factor: 0.135, rebajaUTM:  4.49 },
    { desde:  70.0, hasta:  90.0, factor: 0.230, rebajaUTM: 11.14 },
    { desde:  90.0, hasta: 120.0, factor: 0.304, rebajaUTM: 17.80 },
    { desde: 120.0, hasta: 310.0, factor: 0.350, rebajaUTM: 23.32 },
    { desde: 310.0, hasta: Infinity, factor: 0.400, rebajaUTM: 38.82 }
  ],

  // ── Asignación familiar (tramos vigentes 2026, monto mensual por carga) ─
  asignacionFamiliar: [
    { rentaHasta:  539328, monto: 22007 },
    { rentaHasta:  787746, monto: 13505 },
    { rentaHasta: 1228614, monto:  4267 },
    { rentaHasta:        Infinity, monto:     0 }
  ],

  // ── Gratificación legal (Art. 50 Código del Trabajo) ────────────────────
  // Tope mensual: 25% de la remuneración con tope de 4,75 IMM al año / 12 meses.
  gratificacion: {
    topeAnualIMM: 4.75,
    porcentajeAlternativa: 0.25
  }
};

/* ──────────────────────────────────────────────────────────────────────────
   HELPERS
   ────────────────────────────────────────────────────────────────────────── */

/** Trae UF y UTM del día desde mindicador.cl. Devuelve {uf, utm, fecha}. */
window.MC_fetchIndicadores = async function() {
  const FALLBACK = { uf: 40000, utm: 68000, fecha: null, fallback: true };
  try {
    const [ufR, utmR] = await Promise.all([
      fetch('https://mindicador.cl/api/uf'),
      fetch('https://mindicador.cl/api/utm')
    ]);
    if (!ufR.ok || !utmR.ok) throw new Error('API mindicador');
    const ufJ = await ufR.json();
    const utmJ = await utmR.json();
    return {
      uf:    ufJ.serie[0].valor,
      utm:   utmJ.serie[0].valor,
      fecha: ufJ.serie[0].fecha,
      fallback: false
    };
  } catch (e) {
    return FALLBACK;
  }
};

/** Formatea pesos chilenos. */
window.MC_clp = function(n) {
  return '$ ' + Math.round(n).toLocaleString('es-CL');
};
