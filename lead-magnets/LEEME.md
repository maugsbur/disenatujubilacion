# HTML fuente de las cuatro guías

Estos son los archivos con los que se generaron los PDF. Están en **mm y pt**, que es como conviene editarlos.

## Cómo regenerar un PDF

⚠️ **wkhtmltopdf fuerza un viewport de 1024 px y aplica smart-shrinking que no se puede desactivar.** Hay que convertir mm y pt a px tomando **210 mm ≡ 1024 px** antes de renderizar, o el contenido sale al 77% y no llena la hoja.

La función `to_px()` de `build_common.py` hace esa conversión.

```bash
python3 build_diag.py     # genera autodiagnostico.html y autodiagnostico_px.html
wkhtmltopdf --enable-local-file-access --page-size A4 \
            -T 0 -B 0 -L 0 -R 0 autodiagnostico_px.html autodiagnostico.pdf
```

Lo mismo con `build_plan.py`, `build_hablar.py` y `build_carlos.py`.

## Qué hay acá

| Archivo | Qué es |
|---|---|
| `autodiagnostico-5-pilares.html` | Guía completa, en mm/pt |
| `guia-PLAN-cuatro-acciones.html` | Guía completa, en mm/pt |
| `guia-HABLAR-conversaciones.html` | Guía completa, en mm/pt |
| `guia-ENTUSIASMO-carlos.html` | Guía completa, en mm/pt |
| `build_common.py` | CSS compartido, bloque de CTA y la función `to_px()` |
| `build_*.py` | Contenido de cada guía. **Editar acá, no el HTML** |
| `make_web.py` | Genera las versiones interactivas a partir de los HTML |

## Identidad

- Fuentes: Lora (serif) y Poppins (sans)
- Paleta: `#0E3A2F` verde · `#1A2421` carbón · `#E65F2B` ámbar · `#F6E7B0` crema · `#F8F9FA` off-white
- Las páginas de fondo verde llevan `box-shadow: 0 0 0 5mm` del mismo color, como sangrado. Sin eso queda una franja blanca en el borde
