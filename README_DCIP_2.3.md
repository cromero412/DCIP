# DCIP 2.3 — Nota de versión y guía de archivos

Versión 05/10/2026. Sustituye a DCIP 2.2 (matriz v2.01, arquitectura v2.4). Perímetro de aplicación: empresas de defensa y tecnologías estratégicas de cualquier país.

## Archivos

| Archivo | Contenido | Sustituye a |
|---|---|---|
| `01_DCIP_2.3_Metodologia_y_reglas.pdf` | Principios, perímetro mundial, cálculo completo del scoring, escalas de juicio, cambios, auditoría | 01 Metodología 2.2 |
| `02_DCIP_2.3_Matriz_de_scoring_v3.0.xlsx` | 41 indicadores con rúbrica de cinco niveles, reglas, control con fórmulas, tablas de confianza, bandas, mapeo 2.2 → 2.3 | 02 Matriz v2.01 |
| `03_DCIP_2.3_Diccionario_de_indicadores.pdf` | Magnitudes con equivalencias internacionales y ficha de cada indicador (definición, métrica, polaridad, horizonte, fuente, rúbrica, exclusiones) | 03 Diccionario |
| `04_DCIP_2.3_Jerarquia_de_fuentes_y_evidencia.pdf` | Niveles N1–N6, confianza derivada, antigüedad, desempate, etiquetado, equivalencias por jurisdicción | 04 Jerarquía |
| `DCIP_2.3_Arquitectura_Maestra_v3.0.xlsx` | Expediente operativo: configuración, indicadores, scoring con fórmulas, resultado, evidencia, auditoría, ficha con ratios, riesgos, oportunidades, prospectiva, alertas, fuentes, cambios, histórico, ranking, listas, jurisdicciones y estándar visual | Arquitectura v2.4 |
| `src/dcip_model.py` | Modelo de datos único del que se generan los cinco archivos | — |
| `src/build_*.py` | Generadores (Excel con openpyxl; PDF desde HTML con Chromium) | — |
| `html/` | Fuente editable de los tres PDF | — |

Para cambiar un indicador, un peso, una rúbrica o una tabla: editar `src/dcip_model.py` y ejecutar los tres generadores. Así los cinco archivos no se desincronizan.

## Qué cambia respecto a 2.2

**Matriz.** De 48 a 41 indicadores. Fusiones: las tres capacidades (instalada, efectiva, demostrada) en I01; calidad de cartera y conversión en F08; catalizadores, riesgos prospectivos y señales tempranas en P07. Eliminados: transparencia financiera (es un atributo de la evidencia, pasa a la confianza) y calidad de la tesis (califica al analista, pasa a la auditoría). Ampliado: D10 incorpora control de exportaciones y sanciones. Los pesos de dimensión 25/25/25/25 y los 100 puntos por dimensión no cambian. La tabla completa de correspondencia está en la hoja `Mapeo_2.2_a_2.3` de la matriz y en la parte C del diccionario.

**Rúbricas.** Cada indicador tiene cinco niveles (0 / 25 / 50 / 75 / 100) con descriptores verificables y anclas numéricas en los indicadores financieros. 100 es siempre la situación más favorable; la polaridad de la métrica subyacente se declara.

**Doble conteo.** Cada indicador lista con cuáles no puede compartir evidencia. La auditoría lo comprueba.

**Cálculo.** Nota normalizada y nota prudente (indicadores sin evidencia a 25); rango publicado cuando cruza una banda; cobertura con tres tramos; redondeo definido; DCIP global no concluyente si una dimensión lo es.

**Confianza.** Derivada del nivel de fuente (N1 → MUY ALTA … N6 → MUY BAJA) y de la antigüedad de la evidencia. La hoja de scoring calcula la máxima y marca cuando la introducida la excede.

**Perímetro mundial.** Jurisdicción, norma contable, moneda, tipo de cambio y cierre fiscal en la configuración. Tabla de 24 jurisdicciones con fuentes N1 y N3 equivalentes y tope de confianza. Reglas para perímetro de defensa estimado, propiedad estatal, sanciones e idioma de la evidencia.

**Arquitectura.** Fórmulas reales en scoring, resultado, ficha (ratios), auditoría, riesgos (severidad), histórico y ranking. Validaciones de datos en todas las columnas con lista. Formato condicional con bandas. Trazabilidad scoring → evidencia → fuente. Hoja de cambios entre versiones. Histórico en formato largo que permite comparar y ordenar empresas. Controles de auditoría con marca de crítico y método de comprobación. Plantilla visual con cobertura, mínimo y confianza en el módulo de scoring, y escala de color de bandas separada de los colores de dimensión.

## Filas de ejemplo

Las hojas `05_EVIDENCIA`, `12_FUENTES`, `13_CAMBIOS`, `14_HISTORICO` y `15_RANKING` contienen filas marcadas EJEMPLO con valores ficticios (empresas EJEMPLO_A y EJEMPLO_B) para mostrar el formato y el funcionamiento del ranking. Borrarlas antes de usar el expediente.

## Verificación realizada

Los dos libros se recalcularon con LibreOffice sin errores de fórmula (11.111 fórmulas en la arquitectura, 28 en la matriz). Se probó un expediente ficticio: dimensión completa, dimensión con cobertura del 68 % (con reservas y confianza limitada a MEDIA), dimensión con cobertura del 36 % (no concluyente, DCIP global no concluyente), control de confianza que excede la máxima, ratios del snapshot y ranking de dos empresas. Todos los resultados coincidieron con la regla escrita.
