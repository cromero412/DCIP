# -*- coding: utf-8 -*-
"""Genera los tres PDF (01 Metodología, 03 Diccionario, 04 Fuentes) desde HTML con Chromium headless."""
import html
import os
import subprocess
from pathlib import Path

import dcip_model as M

OUTDIR = Path("/home/user/defensa/DCIP_2.3")
HTMLDIR = OUTDIR / "html"
HTMLDIR.mkdir(exist_ok=True)
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

CSS = f"""
@page {{ size: A4; margin: 18mm 16mm 18mm 16mm; }}
body {{ font-family: Arial, Helvetica, sans-serif; font-size: 10.5pt; color: #1a1a1a; line-height: 1.38; }}
h1 {{ font-size: 19pt; color: #{M.NAVY}; margin: 0 0 2pt 0; letter-spacing: .3px; }}
.sub {{ color: #555; font-size: 9.5pt; margin-bottom: 14pt; border-bottom: 2px solid #{M.NAVY}; padding-bottom: 6pt; }}
h2 {{ font-size: 13pt; color: #{M.NAVY}; margin: 16pt 0 6pt 0; border-left: 4px solid #{M.NAVY}; padding-left: 7pt; page-break-after: avoid; }}
h3 {{ font-size: 11pt; margin: 12pt 0 4pt 0; page-break-after: avoid; }}
p {{ margin: 0 0 6pt 0; text-align: justify; }}
ul {{ margin: 0 0 6pt 0; padding-left: 18pt; }}
li {{ margin-bottom: 2pt; }}
table {{ border-collapse: collapse; width: 100%; margin: 4pt 0 10pt 0; font-size: 9.3pt; page-break-inside: auto; }}
tr {{ page-break-inside: avoid; }}
th {{ background: #{M.NAVY}; color: #fff; text-align: left; padding: 4pt 5pt; vertical-align: top; font-weight: bold; }}
td {{ border: 1px solid #c7ced6; padding: 4pt 5pt; vertical-align: top; }}
.box {{ border: 1px solid #c7ced6; background: #f4f6f8; padding: 7pt 9pt; margin: 8pt 0; }}
.principle {{ background: #{M.NAVY}; color: #fff; padding: 8pt 10pt; font-weight: bold; text-align: center; margin-top: 18pt; }}
.card {{ border: 1px solid #c7ced6; margin: 0 0 9pt 0; page-break-inside: avoid; }}
.card .head {{ color: #fff; padding: 4pt 7pt; font-weight: bold; font-size: 10.5pt; }}
.card .body {{ padding: 5pt 7pt; }}
.card table {{ margin: 4pt 0 2pt 0; }}
.card td.lvl {{ width: 9%; font-weight: bold; text-align: center; background: #f4f6f8; }}
.meta {{ font-size: 9pt; color: #333; }}
.meta b {{ color: #{M.NAVY}; }}
.small {{ font-size: 9pt; color: #555; }}
.FIN {{ background: #{M.DIMENSIONES['FIN']['color']}; }}
.IND {{ background: #{M.DIMENSIONES['IND']['color']}; }}
.DEF {{ background: #{M.DIMENSIONES['DEF']['color']}; }}
.PRO {{ background: #{M.DIMENSIONES['PRO']['color']}; }}
.band {{ display: inline-block; padding: 1pt 6pt; color: #fff; font-weight: bold; }}
.footer {{ font-size: 8.5pt; color: #777; margin-top: 16pt; border-top: 1px solid #c7ced6; padding-top: 4pt; }}
"""


def esc(s):
    return html.escape(str(s)) if s is not None else ""


def table(headers, rows, widths=None):
    out = ["<table>"]
    if widths:
        out.append("<colgroup>" + "".join(f'<col style="width:{w}%">' for w in widths) + "</colgroup>")
    out.append("<tr>" + "".join(f"<th>{esc(h)}</th>" for h in headers) + "</tr>")
    for r in rows:
        out.append("<tr>" + "".join(f"<td>{c if isinstance(c, Raw) else esc(c)}</td>" for c in r) + "</tr>")
    out.append("</table>")
    return "\n".join(out)


class Raw(str):
    pass


def doc(title, subtitle, body, out_name):
    page = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{esc(title)}</title><style>{CSS}</style></head>
<body><h1>{esc(title)}</h1><div class="sub">{esc(subtitle)}</div>{body}
<div class="footer">DCIP {M.VERSION} · {esc(title)} · versión {M.FECHA_VERSION}. Generado desde el modelo común dcip_model.py; cualquier cambio se hace en el modelo y se regeneran los cinco archivos.</div>
</body></html>"""
    h = HTMLDIR / (out_name + ".html")
    h.write_text(page, encoding="utf-8")
    pdf = OUTDIR / (out_name + ".pdf")
    subprocess.run([CHROME, "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", h.as_uri()],
                   check=True, capture_output=True, timeout=120)
    print("OK", pdf)


# =====================================================================================
# 01 METODOLOGÍA Y REGLAS
# =====================================================================================
def metodologia():
    b = []
    b.append(f"<p><b>Objeto.</b> Analizar empresas de defensa y tecnologías estratégicas de cualquier país mediante inteligencia empresarial, financiera, industrial y prospectiva, con un resultado comparable entre empresas, jurisdicciones y fechas.</p>")
    b.append("<h2>1. Reglas fundamentales</h2>")
    b.append("<p><b>No inventar.</b> Diferenciar HECHO / ESTIMACIÓN / INFERENCIA / EXPECTATIVA / HIPÓTESIS en cada afirmación material. Si un dato no puede verificarse, indicarlo y dejar el indicador sin puntuar. Indicar siempre fecha de corte, perímetro, periodo, moneda y norma contable. Priorizar fuentes primarias, oficiales, regulatorias, auditadas y corporativas. Contrastar los datos materiales y buscar activamente evidencia contradictoria.</p>")
    b.append("<p><b>No confundir:</b> propiedad con control; grupo con sociedad individual; contratación con ingresos; cartera con ingresos futuros; cartera firme con opciones, MoU o pipeline; tamaño con competitividad; capacidad potencial con capacidad demostrada; expectativa con hecho; deuda ordinaria con instrumentos híbridos; propiedad pública con dependencia financiera; tecnología industrializada con tecnología en desarrollo.</p>")
    b.append("<h2>2. Perímetro y parámetros del expediente</h2>")
    b.append("<p>Antes del análisis se fijan en 01_CONFIG: empresa, país y jurisdicción; fecha de corte; periodo financiero (último ejercicio cerrado y auditado) y mes de cierre fiscal; norma contable; moneda original y tipo de cambio de referencia del BCE a la fecha de corte; perímetro principal y secundario; peso de defensa en ingresos y su tipo de evidencia. Las comparaciones se hacen con la misma fecha de corte, el mismo perímetro y la misma versión de la metodología. Los ratios se calculan en moneda original; los importes se publican en millones de euros con la moneda original entre paréntesis.</p>")
    b.append("<h2>3. Perímetro mundial: reglas específicas</h2>")
    b.append("<ul>"
             "<li><b>Fuentes por jurisdicción.</b> Cada país tiene fuentes N1 equivalentes (registro mercantil, regulador de mercados, contratación pública y agencia de adquisición). El documento 04 y la hoja 17_JURISDICCIONES las mapean. En jurisdicciones sin publicación fiable, la confianza máxima está topada.</li>"
             "<li><b>Normas contables.</b> IFRS, US GAAP y GAAP locales difieren en resultado operativo, EBITDA, arrendamientos (IFRS 16) y reconocimiento de ingresos de contratos a largo plazo. El diccionario fija la magnitud de referencia y la conversión se declara como ESTIMACIÓN cuando es cálculo propio.</li>"
             "<li><b>Moneda y ejercicio fiscal.</b> Tipo de cambio del BCE en la fecha de corte. Ejercicios que no cierran en diciembre se declaran con su fecha de cierre; la antigüedad de las cuentas se mide desde ese cierre.</li>"
             "<li><b>Propiedad estatal.</b> No penaliza. F07 mide el apoyo financiero no de mercado identificado en cada jurisdicción (subvenciones, recapitalizaciones para cubrir pérdidas, préstamos blandos, avales ejecutados, prefinanciación a coste cero).</li>"
             "<li><b>Perímetro de defensa.</b> En grupos diversificados sin segmento publicado, se estima el peso de defensa, se etiqueta ESTIMACIÓN y se declara el método. D02, D03, D07 y D12 se calculan sobre ese perímetro.</li>"
             "<li><b>Sanciones y control de exportaciones.</b> Se verifican en listas oficiales (UE, OFAC, ONU, Reino Unido) y en los regímenes ITAR y EAR. Se evalúan en D10; su efecto financiero cuantificado, en F10.</li>"
             "<li><b>Idioma de la evidencia.</b> Se registra el idioma original y si la cita es traducción. Una traducción propia de una cifra material se contrasta con la fuente original.</li>"
             "</ul>")
    b.append("<h2>4. Análisis</h2>")
    b.append("<p>Situación empresarial; propiedad y control; finanzas; defensa y programas; contratación y cartera; capacidad industrial; tecnología e I+D+i; internacionalización; competencia; cadena de suministro; riesgos; oportunidades; prospectiva. Cada bloque se documenta en 07_FICHA con su tipo de evidencia dominante.</p>")
    b.append("<h2>5. Finanzas</h2>")
    b.append("<p>Separar cifra de negocio, contratación, cartera y cartera firme, resultado operativo, resultado neto, flujo de caja operativo, deuda financiera y deuda neta, instrumentos híbridos, liquidez, patrimonio y apoyo público. EBITDA solo si está publicado o se presenta como cálculo propio. Cartera no equivale a ingreso garantizado. Los ratios de 07_FICHA alimentan las anclas numéricas de F01 a F10.</p>")
    b.append("<h2>6. Capacidad industrial</h2>")
    b.append("<p>Distinguir capacidad instalada, potencial, efectiva, demostrada y disponible. Se puntúa en un único indicador (I01) evaluando la cadena instalada → efectiva → demostrada: la nota la fija el eslabón más débil. Considerar instalaciones, plantilla, cualificación, productividad, cuellos de botella, proveedores, integración, plazos y carga de trabajo.</p>")
    b.append("<h2>7. Defensa</h2>")
    b.append("<p>Evaluar programas estratégicos, cartera militar firme, sostenimiento, integración de sistemas, tecnologías críticas, clientes gubernamentales, exportación, interoperabilidad, propiedad intelectual, autonomía y control de exportaciones, pipeline y concentración. Distinguir contratos, opciones, MoU, acuerdos industriales y expectativas. La calificación de programa estratégico y de tecnología crítica procede de documentación oficial, no de la empresa.</p>")
    b.append("<h2>8. Prospectiva</h2>")
    b.append("<p>Escenarios BASE / ALCISTA / BAJISTA para 12–24 meses, 3–5 años y 5–10 años, con impulsores, riesgos, catalizadores, señales tempranas y factores de invalidación (10_PROSPECTIVA). No asignar probabilidades numéricas: usar BAJA / MEDIA / ALTA. Las señales tempranas se gestionan en 11_ALERTA_TEMPRANA con trigger, fuente y frecuencia; no son un indicador de scoring.</p>")

    b.append("<h2>9. Valoración: estructura y cálculo</h2>")
    b.append(f"<p><b>Estructura.</b> DCIP = 25 % FIN + 25 % IND + 25 % DEF + 25 % PRO. Cada dimensión tiene 100 puntos repartidos entre sus indicadores ({len(M.INDICADORES)} en total: FIN 10, IND 10, DEF 12, PRO 9). Cada indicador se puntúa 0–100 con una rúbrica de cinco niveles (0 / 25 / 50 / 75 / 100) definida en el diccionario; 100 es siempre la situación más favorable.</p>")
    b.append("<p><b>Cálculo.</b></p><ol>"
             "<li>Nota normalizada de dimensión = Σ(puntuación × peso) / Σ(pesos de los indicadores puntuados).</li>"
             f"<li>Nota prudente de dimensión = (Σ(puntuación × peso) + {M.PUNT_PRUDENTE_FALTANTE} × Σ(pesos de los indicadores sin puntuar)) / 100.</li>"
             "<li>Cobertura = Σ(pesos puntuados) / 100. Si es inferior al 60 %, la dimensión es NO CONCLUYENTE y no se calcula el DCIP global. Entre el 60 % y el 79 %, la confianza máxima es MEDIA.</li>"
             "<li>DCIP normalizado = 0,25 × Σ notas normalizadas; DCIP prudente = 0,25 × Σ notas prudentes. Ambos se redondean al entero más próximo, mitad hacia arriba.</li>"
             "<li>La categoría se asigna sobre el entero. Si el DCIP prudente y el normalizado caen en bandas distintas, se publica el rango (por ejemplo, 'Estable – Favorable (rango)') y no se fuerza una banda.</li>"
             "<li>Si la evidencia de un indicador solo permite un intervalo, se registran mínimo y máximo y se puntúa el punto central.</li></ol>")
    rows = [(Raw(f'<span class="band" style="background:#{col}">{nom}</span>'), f"{lo}–{hi}") for lo, hi, nom, col, _ in M.BANDAS]
    b.append(table(["Banda", "Intervalo (entero)"], rows, [40, 60]))
    b.append("<p><b>Doble conteo.</b> Un hecho no puede mejorar dos indicadores declarados excluyentes en el diccionario (columna 'no comparte evidencia con'). La auditoría comprueba que ningún EVIDENCIA_ID sustenta dos indicadores excluyentes.</p>")

    b.append("<h2>10. Confianza</h2>")
    b.append("<p>MUY ALTA / ALTA / MEDIA / BAJA / MUY BAJA. Se deriva de la evidencia, nunca de la puntuación. Para cada indicador, la confianza máxima la fija el nivel de la fuente principal y la antigüedad de la evidencia respecto a la fecha de corte (documento 04). La confianza de la dimensión es la media ponderada de la de sus indicadores, redondeada hacia abajo y limitada por la cobertura. La confianza global es la menor de las cuatro dimensiones.</p>")
    b.append("<h2>11. Juicios</h2>")
    b.append("<p>Se emiten de forma independiente y con escalas de cinco niveles. <b>Estado empresarial</b> describe la situación económica e industrial actual y se informa principalmente de FIN e IND. <b>Atractividad estratégica</b> describe el valor futuro para defensa, tecnología e industria y se informa principalmente de DEF y PRO. Ninguno se calcula: son juicios del analista razonados sobre el scoring.</p>")
    b.append(table(["Estado empresarial", "Descripción"], M.ESCALA_ESTADO, [25, 75]))
    b.append(table(["Atractividad estratégica", "Descripción"], M.ESCALA_ATRACTIVIDAD, [25, 75]))
    b.append("<h2>12. Cambios entre versiones de expediente</h2>")
    b.append("<p>Cada actualización incrementa la versión del expediente y registra en 13_CAMBIOS, por indicador, dimensión y DCIP: valor anterior, valor nuevo, tipo de cambio (REAL o METODOLÓGICO) y calificación (MEJORA / ESTABLE / DETERIORO / DETERIORO CRÍTICO / NUEVA INFORMACIÓN). Un cambio metodológico se aplica retroactivamente a la versión anterior antes de comparar, para que el cambio real quede aislado.</p>")
    b.append("<h2>13. Alerta temprana</h2>")
    b.append("<p>Vigilar contratos, cancelaciones, retrasos, sobrecostes, cartera, márgenes, caja, deuda, plantilla, inversiones, capacidad, exportaciones, programas, regulación y sanciones, y presupuestos. Cada señal tiene prioridad, trigger, fuente de seguimiento, frecuencia y acción.</p>")
    b.append("<h2>14. Comparaciones y rankings</h2>")
    b.append("<p>Misma fecha de corte, misma versión de metodología, mismos indicadores. Las puntuaciones por indicador de cada expediente se vuelcan en 14_HISTORICO en formato largo; 15_RANKING calcula notas, cobertura y posición. No se comparan expedientes con dimensiones NO CONCLUYENTES. Separar en la lectura tamaño, rentabilidad, finanzas, industria, tecnología, defensa, internacionalización y riesgo.</p>")
    b.append("<h2>15. Auditoría y validez</h2>")
    b.append("<p>El expediente pasa 22 controles (06_AUDITORIA). Si un control crítico no se cumple, el expediente es NO VÁLIDO y no se publica ni se representa gráficamente.</p>")
    b.append("<h2>16. Salida</h2>")
    b.append("<p>Resumen ejecutivo; perímetro y parámetros; situación; propiedad y control; finanzas; defensa y programas; industria y tecnología; mercado e internacionalización; competencia; riesgos y oportunidades; prospectiva; alertas; FIN, IND, DEF, PRO con nota, mínimo, cobertura y confianza; DCIP global con rango y categoría; estado empresarial; atractividad estratégica; confianza global; juicio final; fuentes con nivel y fecha.</p>")
    b.append("<h2>Anexo. Comandos de uso con asistente</h2>")
    b.append("<p class='small'>Analizar: EMPRESA | Actualizar: EMPRESA | Propiedad: EMPRESA | Finanzas: EMPRESA | Defensa: EMPRESA | Industria: EMPRESA | Prospectiva: EMPRESA | Comparar: A vs B | Ranking: EMPRESAS | Cambios: EMPRESA | Auditar: EMPRESA. Cada comando produce exclusivamente las hojas y secciones indicadas en esta metodología.</p>")
    b.append('<div class="principle">ES PREFERIBLE RECONOCER UNA INCERTIDUMBRE QUE RELLENARLA CON UN DATO NO DEMOSTRADO.</div>')
    doc(f"DCIP {M.VERSION} — Metodología y reglas", f"Versión {M.FECHA_VERSION}. Sustituye a DCIP 2.2. Perímetro: empresas de defensa y tecnologías estratégicas de cualquier país.", "\n".join(b), f"01_DCIP_{M.VERSION}_Metodologia_y_reglas")


# =====================================================================================
# 03 DICCIONARIO DE INDICADORES
# =====================================================================================
def diccionario():
    b = []
    b.append("<p><b>Objetivo.</b> Fijar definiciones homogéneas de magnitudes y, por primera vez, una ficha operativa de cada uno de los indicadores: definición, métrica, polaridad, horizonte, fuente preferente, rúbrica de cinco niveles e indicadores con los que no comparte evidencia. Sin esta ficha, dos analistas no puntuarían igual y el scoring no sería reproducible.</p>")
    b.append("<h2>Parte A. Magnitudes</h2>")
    b.append(table(["Magnitud", "Definición", "Nota internacional"], M.MAGNITUDES, [18, 48, 34]))
    b.append("<h2>Parte B. Fichas de los indicadores</h2>")
    b.append("<p class='small'>Lectura de la rúbrica: se elige el nivel cuya descripción acredita la evidencia citada. Valores intermedios solo si la evidencia sitúa a la empresa entre dos niveles; entonces se registra el rango. 100 es siempre la situación más favorable, también cuando la métrica subyacente es 'menor es mejor'.</p>")
    for d, info in M.DIMENSIONES.items():
        inds = [i for i in M.INDICADORES if i["dim"] == d]
        b.append(f"<h3>{d} — Dimensión {info['nombre'].lower()} ({len(inds)} indicadores, 100 puntos)</h3>")
        for i in inds:
            rub = "".join(f'<tr><td class="lvl">{lvl}</td><td>{esc(i["rubrica"][lvl])}</td></tr>' for lvl in (0, 25, 50, 75, 100))
            nd = ", ".join(i["no_doble"]) if i["no_doble"] else "ninguno"
            nota = f'<p class="small"><b>Nota.</b> {esc(i["nota"])}</p>' if i["nota"] else ""
            b.append(f"""<div class="card"><div class="head {d}">{i['id']} · {esc(i['nombre'])} · peso {i['peso']}</div><div class="body">
<p class="meta"><b>Definición.</b> {esc(i['definicion'])}</p>
<p class="meta"><b>Métrica.</b> {esc(i['metrica'])}</p>
<p class="meta"><b>Polaridad de la métrica:</b> {esc(i['polaridad'])} · <b>Horizonte:</b> {esc(i['horizonte'])} · <b>Fuente preferente:</b> {i['fuente']} · <b>No comparte evidencia con:</b> {nd}</p>
<table><colgroup><col style="width:9%"><col style="width:91%"></colgroup>{rub}</table>{nota}</div></div>""")
    b.append("<h2>Parte C. Correspondencia con la matriz 2.2</h2>")
    rows = [(d, n, p, dest, p2 if p2 is not None else "", c) for d, n, p, dest, p2, c in M.MAPEO_22_23]
    b.append(table(["Dim.", "Indicador 2.2", "Peso 2.2", "Destino", "Peso 2.3", "Cambio"], rows, [6, 24, 8, 8, 8, 46]))
    doc(f"DCIP {M.VERSION} — Diccionario de magnitudes e indicadores", f"Versión {M.FECHA_VERSION}. {len(M.INDICADORES)} indicadores con rúbrica, polaridad, anclas y reglas de no doble conteo.", "\n".join(b), f"03_DCIP_{M.VERSION}_Diccionario_de_indicadores")


# =====================================================================================
# 04 JERARQUÍA DE FUENTES Y EVIDENCIA
# =====================================================================================
def fuentes():
    b = []
    b.append("<p><b>Objetivo.</b> Establecer una jerarquía codificada de fuentes (N1–N6) válida para cualquier jurisdicción, derivar de ella la confianza y fijar las reglas de desempate, antigüedad y etiquetado.</p>")
    b.append("<h2>1. Niveles de fuente y confianza máxima</h2>")
    b.append(table(["Código", "Nivel", "Qué incluye", "Confianza máxima"], M.NIVELES_FUENTE, [8, 20, 56, 16]))
    b.append("<h2>2. Antigüedad de la evidencia</h2>")
    b.append("<p>Se mide en meses entre la fecha de la evidencia y la fecha de corte. La penalización se resta a la confianza máxima del nivel de fuente; el resultado nunca baja de MUY BAJA.</p>")
    b.append(table(["Antigüedad", "Penalización (niveles de confianza)"], M.ANTIGUEDAD, [60, 40]))
    b.append("<h2>3. Cobertura y confianza de la dimensión</h2>")
    b.append(table(["Cobertura de la dimensión", "Efecto"], M.COBERTURA, [25, 75]))
    b.append("<p>La confianza de un indicador es la que asigna el analista sin superar la máxima calculada. La de la dimensión es la media ponderada de sus indicadores, redondeada hacia abajo y limitada por la cobertura. La global es la menor de las cuatro. Una contradicción material no resuelta rebaja un nivel la confianza del indicador afectado.</p>")
    b.append("<h2>4. Reglas por tipo de dato</h2>")
    b.append("<ul>"
             "<li><b>Cifras financieras:</b> cuentas auditadas (N1). Presentaciones a inversores (N2) solo para desgloses no auditados, etiquetados como tales.</li>"
             "<li><b>Contratos y adjudicaciones:</b> órgano contratante o boletín oficial (N1). Comunicados de la empresa (N2) para importes y plazos no publicados oficialmente, etiquetados EXPECTATIVA si el contrato no está firmado.</li>"
             "<li><b>Propiedad y control:</b> registros mercantiles y regulador de mercados (N1).</li>"
             "<li><b>Cartera:</b> comprobar definición y perímetro en la fuente; sin desglose firme / no firme, tope de puntuación en F08 y etiqueta ESTIMACIÓN.</li>"
             "<li><b>Tecnología:</b> evidencia de programa, producto, demostrador o contrato (N1–N3). La calificación de crítica procede de documentos oficiales.</li>"
             "<li><b>Capacidad industrial:</b> entregas acreditadas por el cliente o auditoría pública (N1) antes que declaraciones corporativas (N2).</li>"
             "<li><b>Previsiones:</b> identificar quién las formula y etiquetar EXPECTATIVA. Consenso de analistas es N4.</li>"
             "<li><b>Sanciones y control de exportaciones:</b> listas oficiales de la UE, OFAC, ONU y Reino Unido; registros ITAR y EAR (N1).</li>"
             "</ul>")
    b.append("<h2>5. Reglas de desempate entre fuentes</h2>")
    b.append("<ol>"
             "<li>Entre niveles distintos prevalece el de menor número (N1 sobre N2, etc.).</li>"
             "<li>Entre fuentes del mismo nivel prevalece la más reciente respecto a la fecha de corte, salvo que la más antigua esté auditada y la reciente no.</li>"
             "<li>Entre una cifra auditada anterior y una no auditada posterior se publican ambas: la auditada puntúa, la posterior se registra como EXPECTATIVA o ESTIMACIÓN.</li>"
             "<li>Entre perímetros distintos no hay desempate: se declara la diferencia y se usa el perímetro de 01_CONFIG.</li>"
             "<li>Toda discrepancia material se registra en CONTRADICCION con su RESOLUCION. Una contradicción no resuelta rebaja la confianza y se menciona en el juicio.</li>"
             "</ol>")
    b.append("<h2>6. Etiquetado de la evidencia</h2>")
    b.append(table(["Etiqueta", "Significado"], [
        ("HECHO", "Respaldado directamente por una fuente N1 a N3 con cita y referencia."),
        ("ESTIMACIÓN", "Cálculo propio a partir de datos: ratios, conversiones, EBITDA calculado, peso de defensa estimado, traducciones."),
        ("INFERENCIA", "Conclusión derivada de varios hechos; se explicita el razonamiento."),
        ("EXPECTATIVA", "Previsión formulada por una fuente identificada: guía corporativa, presupuesto, consenso."),
        ("HIPÓTESIS", "Escenario no demostrado, construido por el analista para la prospectiva."),
    ], [20, 80]))
    b.append("<h2>7. Jurisdicciones: fuentes N1 y N3 equivalentes</h2>")
    b.append("<p class='small'>El tope de confianza FIN se aplica a la dimensión financiera salvo que existan cuentas auditadas verificables. Para países no listados se aplica la regla general y se añade la fila a 17_JURISDICCIONES del expediente.</p>")
    rows = [(p, nc, reg, regu, con, inst, tope, nota) for p, nc, reg, regu, con, inst, tope, nota in M.JURISDICCIONES]
    b.append(table(["País", "Norma contable", "Registro y cuentas (N1)", "Regulador (N1)", "Contratación y defensa (N1)", "Institucional (N3) / sectorial (N4)", "Tope FIN", "Nota"], rows, [9, 9, 15, 11, 18, 16, 8, 14]))
    b.append("<h2>8. Fuentes supranacionales y sectoriales de uso general</h2>")
    b.append("<ul>"
             "<li><b>N3:</b> Agencia Europea de Defensa (EDA), Fondo Europeo de Defensa (EDF) y PESCO; OCCAR; NSPA y OTAN; Tribunal de Cuentas Europeo; bancos centrales (tipos de cambio); GAO, NAO, Cour des comptes y equivalentes.</li>"
             "<li><b>N4:</b> SIPRI (Arms Industry Database, Arms Transfers Database); IISS Military Balance; ASD, AIA, NDIA, TEDAE, GIFAS, BDSV, ADS; bases de datos sectoriales de pago, citadas con fecha de consulta.</li>"
             "<li><b>N5:</b> prensa económica y de defensa; útil para cronología y contexto, nunca como fundamento único de una cifra o un contrato.</li>"
             "</ul>")
    b.append('<div class="principle">LA CALIDAD DE LA CONCLUSIÓN NUNCA PUEDE SUPERAR LA CALIDAD DE LA EVIDENCIA.</div>')
    doc(f"DCIP {M.VERSION} — Jerarquía de fuentes y evidencia", f"Versión {M.FECHA_VERSION}. Niveles N1–N6, confianza derivada, antigüedad, desempate y equivalencias por jurisdicción.", "\n".join(b), f"04_DCIP_{M.VERSION}_Jerarquia_de_fuentes_y_evidencia")


if __name__ == "__main__":
    M.check()
    metodologia()
    diccionario()
    fuentes()
