"""Lead magnet "¿Y si ya tienes suficiente?": cuánto cuesta un mes de tu vida.

Salida: lead-magnets/planilla-ya-tienes-suficiente.xlsx

Una sola hoja, de arriba hacia abajo, para completarla en unos 15 minutos:
1. Tu mes hoy  2. Tu mes sin trabajo  3. Lo que ya tienes  4. El resultado.
Todo con fórmulas, sin macros: funciona en Excel y en Google Sheets.

Encuadre aprobado por Marcel el 28/09/2026: le habla a quien ya tiene la
plata resuelta y sigue trabajando por inercia, no a "¿me va a alcanzar?".
Criterios en Notion, 🎬 Cómo creamos contenido › 10b Lead magnets.

Límite: es aritmética simple en pesos de hoy. No es asesoría financiera ni
previsional, y la planilla lo dice.
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

import sys
sys.path.insert(0, str(Path(__file__).parent))
from build_common import cal_url  # noqa: E402

OUT = Path(__file__).with_name("planilla-ya-tienes-suficiente.xlsx")

VERDE = "0E3A2F"
CARBON = "1A2421"
AMBAR = "E65F2B"
CREMA = "F6E7B0"
CLARO = "F8F9FA"

F_TITULO = Font(name="Lora", size=20, bold=True, color=CREMA)
F_BAJADA = Font(name="Poppins", size=11, color=CLARO)
F_PASO = Font(name="Lora", size=14, bold=True, color=VERDE)
F_AYUDA = Font(name="Poppins", size=9, italic=True, color="4A5A55")
F_HEAD = Font(name="Poppins", size=10, bold=True, color=CLARO)
F_TXT = Font(name="Poppins", size=10, color=CARBON)
F_LABEL = Font(name="Poppins", size=10, bold=True, color=CARBON)
F_BIG = Font(name="Lora", size=16, bold=True, color=VERDE)
F_FRASE = Font(name="Lora", size=13, bold=True, color=VERDE)
F_CTA = Font(name="Poppins", size=11, bold=True, color=AMBAR, underline="single")
F_NOTA = Font(name="Poppins", size=8, italic=True, color="4A5A55")
FILL_VERDE = PatternFill("solid", fgColor=VERDE)
FILL_INPUT = PatternFill("solid", fgColor="FFF6D6")
FILL_OUT = PatternFill("solid", fgColor="EAF1EE")
LINEA = Side(style="thin", color="C9D3CF")
BORDE = Border(left=LINEA, right=LINEA, top=LINEA, bottom=LINEA)
WRAP = Alignment(wrap_text=True, vertical="center")
PESOS = '"$" #,##0'

# Categoría, ayuda. Lo mensual va en C, lo que se paga una o pocas veces al
# año va en D, y E lo lleva a mes.
GASTOS = [
    ("Vivienda", "dividendo o arriendo, gastos comunes; contribuciones en la columna anual"),
    ("Cuentas de la casa", "luz, agua, gas, internet, teléfono"),
    ("Supermercado y feria", ""),
    ("Salud", "isapre o Fonasa, seguros, remedios, consultas"),
    ("Transporte", "auto, bencina, TAG, mantención; permiso y seguro en la anual"),
    ("Ayuda a tu familia", "hijos, padres, otros"),
    ("Comer fuera y panoramas", ""),
    ("Viajes", "lo del año, en la columna anual"),
    ("Regalos y celebraciones", ""),
    ("Ropa y cuidado personal", ""),
    ("Imprevistos y reparaciones", "lo que se rompe; en la anual"),
    ("Otros", ""),
]


def build():
    wb = Workbook()
    ws = wb.active
    ws.title = "Tu número"
    ws.sheet_view.showGridLines = False
    for col, w in zip("ABCDE", (3, 46, 15, 15, 22)):
        ws.column_dimensions[col].width = w

    def celda(ref, valor=None, font=F_TXT, fill=None, fmt=None, align=WRAP, borde=False):
        c = ws[ref]
        if valor is not None:
            c.value = valor
        c.font = font
        c.alignment = align
        if fill:
            c.fill = fill
        if fmt:
            c.number_format = fmt
        if borde:
            c.border = BORDE
        return c

    # Portada en franja verde
    for r in range(1, 5):
        for col in "ABCDE":
            ws[f"{col}{r}"].fill = FILL_VERDE
    ws.merge_cells("B2:E2")
    celda("B2", "¿Y si ya tienes suficiente?", F_TITULO, FILL_VERDE)
    ws.merge_cells("B3:E3")
    celda("B3", "Cuánto cuesta un mes de tu vida, y cuántos años de esa vida ya tienes "
                "cubiertos. Toma unos 15 minutos. Completa solo las celdas amarillas.",
          F_BAJADA, FILL_VERDE)
    ws.row_dimensions[2].height = 34
    ws.row_dimensions[3].height = 34

    # Paso 1
    r = 6
    ws.merge_cells(f"B{r}:E{r}")
    celda(f"B{r}", "1 · Tu mes hoy", F_PASO)
    ws.merge_cells(f"B{r+1}:E{r+1}")
    celda(f"B{r+1}", "Primer paso: abre la aplicación de tu banco y mira el último mes cerrado. "
                     "Un número redondo basta.", F_AYUDA)
    r += 2
    for col, txt in zip("BCDE", ("Gasto", "Al mes", "Al año", "Mensual")):
        celda(f"{col}{r}", txt, F_HEAD, FILL_VERDE, borde=True)
    primera = r + 1
    for nombre, ayuda in GASTOS:
        r += 1
        etiqueta = nombre if not ayuda else f"{nombre}\n({ayuda})"
        celda(f"B{r}", etiqueta, F_TXT, borde=True)
        celda(f"C{r}", None, F_TXT, FILL_INPUT, PESOS, borde=True)
        celda(f"D{r}", None, F_TXT, FILL_INPUT, PESOS, borde=True)
        celda(f"E{r}", f"=N(C{r})+N(D{r})/12", F_TXT, FILL_OUT, PESOS, borde=True)
        ws.row_dimensions[r].height = 42 if ayuda else 20
    ultima = r
    r += 1
    celda(f"B{r}", "Cuánto cuesta un mes de tu vida hoy", F_LABEL, borde=True)
    ws.merge_cells(f"C{r}:D{r}")
    celda(f"E{r}", f"=SUM(E{primera}:E{ultima})", F_BIG, FILL_OUT, PESOS, borde=True)
    fila_mes_hoy = r
    ws.row_dimensions[r].height = 26

    # Paso 2
    r += 2
    ws.merge_cells(f"B{r}:E{r}")
    celda(f"B{r}", "2 · Tu mes sin trabajo", F_PASO)
    r += 1
    ws.merge_cells(f"B{r}:E{r}")
    celda(f"B{r}", "Al dejar de trabajar, algunos gastos se van y otros aparecen. Una estimación basta.",
          F_AYUDA)
    r += 1
    celda(f"B{r}", "Lo que dejarías de gastar al mes\n(traslados, almuerzos, ropa de trabajo)", borde=True)
    celda(f"E{r}", None, F_TXT, FILL_INPUT, PESOS, borde=True)
    fila_menos = r
    ws.row_dimensions[r].height = 36
    r += 1
    celda(f"B{r}", "Lo que agregarías al mes\n(viajes, actividades, salud, tiempo libre)", borde=True)
    celda(f"E{r}", None, F_TXT, FILL_INPUT, PESOS, borde=True)
    fila_mas = r
    ws.row_dimensions[r].height = 36
    r += 1
    celda(f"B{r}", "Cuánto costaría un mes de tu vida sin trabajo", F_LABEL, borde=True)
    celda(f"E{r}", f"=MAX(0,E{fila_mes_hoy}-N(E{fila_menos})+N(E{fila_mas}))",
          F_BIG, FILL_OUT, PESOS, borde=True)
    fila_mes_sin = r
    ws.row_dimensions[r].height = 26

    # Paso 3
    r += 2
    ws.merge_cells(f"B{r}:E{r}")
    celda(f"B{r}", "3 · Lo que ya tienes", F_PASO)
    r += 1
    ws.merge_cells(f"B{r}:E{r}")
    celda(f"B{r}", "Lo que puedes usar para vivir, sin contar la casa donde vives.", F_AYUDA)
    filas = {}
    for clave, texto, fmt, h in (
        ("ahorro", "Ahorro e inversiones disponibles\n(sin la casa donde vives)", PESOS, 36),
        ("pension", "Pensión mensual estimada\n(la que te informa tu AFP o tu cartola)", PESOS, 36),
        ("otros", "Otros ingresos mensuales que seguirían\n(arriendos, rentas)", PESOS, 36),
        ("anios", "¿Cuántos años quieres financiar?\n(por ejemplo, hasta los 90)", "0", 36),
    ):
        r += 1
        celda(f"B{r}", texto, borde=True)
        celda(f"E{r}", None, F_TXT, FILL_INPUT, fmt, borde=True)
        filas[clave] = r
        ws.row_dimensions[r].height = h
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="50",
                        showErrorMessage=True, error="Un número de años entre 1 y 50.")
    ws.add_data_validation(dv)
    dv.add(f"E{filas['anios']}")

    # Paso 4
    r += 2
    ws.merge_cells(f"B{r}:E{r}")
    celda(f"B{r}", "4 · Tu resultado", F_PASO)
    r += 1
    celda(f"B{r}", "Lo que te falta cada mes, después de pensión y otros ingresos", borde=True)
    celda(f"E{r}", f"=MAX(0,E{fila_mes_sin}-N(E{filas['pension']})-N(E{filas['otros']}))",
          F_TXT, FILL_OUT, PESOS, borde=True)
    fila_brecha = r
    ws.row_dimensions[r].height = 36
    r += 1
    celda(f"B{r}", "Años de esa vida que ya tienes cubiertos", F_LABEL, borde=True)
    celda(f"E{r}",
          f'=IF(E{fila_mes_sin}=0,"",IF(E{fila_brecha}=0,"Todos",N(E{filas["ahorro"]})/E{fila_brecha}/12))',
          F_BIG, FILL_OUT, "0.0", borde=True)
    fila_cubre = r
    ws.row_dimensions[r].height = 26
    r += 2
    ws.merge_cells(f"B{r}:E{r}")
    frase = (
        f'=IF(E{fila_mes_sin}=0,"Completa los pasos 1 a 3 y aquí aparece tu resultado.",'
        f'IF(AND(N(E{filas["ahorro"]})=0,N(E{filas["pension"]})=0,N(E{filas["otros"]})=0),"Completa el paso 3 con lo que ya tienes y aquí aparece tu resultado.",'
        f'IF(E{fila_brecha}=0,"Tu pensión y tus otros ingresos ya cubren tu mes. La plata no es lo que te retiene.",'
        f'IF(N(E{filas["anios"]})=0,"Tu ahorro cubre "&ROUND(E{fila_cubre},1)&" años de tu vida sin trabajar. Anota cuántos años quieres financiar para compararlo.",'
        f'IF(E{fila_cubre}>=E{filas["anios"]},"Ya tienes suficiente para los "&E{filas["anios"]}&" años que quieres financiar. Si sigues trabajando, no es por la plata.",'
        f'"Tu ahorro cubre "&ROUND(E{fila_cubre},1)&" de los "&E{filas["anios"]}&" años que quieres financiar.")))))'
    )
    celda(f"B{r}", frase, F_FRASE)
    ws.row_dimensions[r].height = 48

    # Cierre
    r += 2
    ws.merge_cells(f"B{r}:E{r}")
    celda(f"B{r}", "El número responde cuánto. No responde para qué: qué vida vas a financiar con "
                   "él, y quién vas a ser cuando el trabajo ya no ordene tu semana. Postergarlo un "
                   "año más también es una elección, y se paga con años de salud y energía.",
          F_TXT)
    ws.row_dimensions[r].height = 58
    r += 1
    ws.merge_cells(f"B{r}:E{r}")
    c = celda(f"B{r}", "Si quieres mirar tu caso, agenda una llamada de evaluación gratuita de 45 minutos "
                       "con Margarita, que coordina el programa.", F_LABEL)
    ws.row_dimensions[r].height = 32
    r += 1
    ws.merge_cells(f"B{r}:E{r}")
    c = celda(f"B{r}", "Agendar la llamada", F_CTA)
    c.hyperlink = cal_url("planilla-suficiente")
    r += 2
    ws.merge_cells(f"B{r}:E{r}")
    celda(f"B{r}", "Cálculo simple, en pesos de hoy: no considera inflación, rentabilidad ni impuestos. "
                   "Es orientación personal, no asesoría financiera ni previsional. Para decidir cuándo "
                   "y cómo jubilar, conversa con un asesor previsional. · Diseña tu Jubilación",
          F_NOTA)
    ws.row_dimensions[r].height = 36

    ws.print_area = f"A1:E{r}"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToHeight = 0
    ws.freeze_panes = None
    wb.save(OUT)
    return OUT


if __name__ == "__main__":
    print(build())
