# 📖 Referencia Técnica: CLI y API de Python

Este documento contiene la especificación técnica exacta de los comandos, opciones, estructura de directorios y clases internas de **`pdfflatten`**.

---

## 1. Interfaz de Línea de Comandos (CLI)

### Sintaxis

```bash
pdfflatten [path] [-o OUTPUT] [-b] [--input-dir INPUT_DIR] [--output-dir OUTPUT_DIR] [--processed-dir PROCESSED_DIR] [--dpi DPI] [-v] [-V] [-h]
```

También ejecutable como módulo:

```bash
python -m pdfflatten [opciones]
```

### Tabla de Argumentos y Opciones

| Argumento / Flag | Tipo | Valor por defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `path` | `Path` | `None` | Ruta del archivo PDF individual a procesar. Requerido si no se usa `-b/--batch`. |
| `-o`, `--output` | `Path` | `runtime/output/<nombre>.pdf` | Ruta del archivo de salida o carpeta destino en modo individual. |
| `-b`, `--batch` | `bool` | `False` | Procesa todos los archivos `.pdf` del directorio de entrada. |
| `--input-dir` | `Path` | `runtime/input` | Directorio de entrada para el modo `--batch`. |
| `--output-dir` | `Path` | `runtime/output` | Directorio de salida para el modo `--batch`. |
| `--processed-dir` | `Path` | `runtime/processed` | Directorio donde se mueven los PDFs originales tras procesarse en modo `--batch`. |
| `--dpi` | `int` | `300` | Resolución de rasterizado en puntos por pulgada (*dots per inch*). Debe ser `> 0`. |
| `-v`, `--verbose` | `bool` | `False` | Activa el nivel `DEBUG` en la salida de consola. |
| `-V`, `--version` | `action` | — | Muestra la versión (`pdfflatten 0.1.0`) y finaliza con código `0`. |
| `-h`, `--help` | `action` | — | Muestra la ayuda de uso y finaliza con código `0`. |

### Códigos de Salida

| Código | Condición |
| :---: | :--- |
| `0` | Ejecución completada sin errores. |
| `1` | Error controlado: falta de argumentos (`path` o `--batch`), `--dpi <= 0`, archivo inexistente o fallo durante la conversión de algún PDF. |

---

## 2. Estructura de `runtime/` y Logging

Al iniciarse, `Config.ensure_runtime_dirs()` garantiza la existencia de los siguientes directorios locales (excluidos de Git):

| Clave en `Config.PATHS` | Ruta por defecto | Propósito |
| :--- | :--- | :--- |
| `"input"` | `runtime/input/` | Entrada por defecto en modo `--batch`. |
| `"output"` | `runtime/output/` | Salida por defecto para archivos aplanados. |
| `"processed"` | `runtime/processed/` | Archivo histórico de PDFs originales ya procesados en `--batch`. |
| `"logs"` | `runtime/logs/` | Carpeta contenedora de archivos de registro. |
| `"app_log"` | `runtime/logs/app.log` | Archivo rotativo de logs (`RotatingFileHandler`, máx. 5 MB, 3 respaldos, nivel `DEBUG`). |

---

## 3. API de Python (`pdfflatten`)

### Clase `pdfflatten.Converter`

Ubicación: `src/pdfflatten/converter.py`

#### `Converter.flatten_pdf(input_pdf: Path | str, output_pdf: Path | str, dpi: int = 300) -> Path`
Aplana un archivo PDF de principio a fin utilizando un directorio temporal seguro (`tempfile.TemporaryDirectory(prefix="pdfflatten_")`) que se elimina automáticamente al finalizar.

```python
from pathlib import Path
from pdfflatten import Converter

resultado = Converter.flatten_pdf(
    input_pdf=Path("contrato.pdf"),
    output_pdf=Path("contrato_plano.pdf"),
    dpi=300,
)
```

#### `Converter.convert_pdf_to_images(pdf_path: Path | str, output_folder: Path | str, dpi: int = 300) -> list[Path]`
Renderiza cada página del PDF como una imagen PNG (`page_0001.png`, `page_0002.png`, ...) dentro de `output_folder`.
- **Excepciones:** `FileNotFoundError` si `pdf_path` no existe; `ValueError` si `dpi <= 0`.

#### `Converter.convert_images_to_pdf(image_folder: Path | str, output_pdf_path: Path | str) -> Path`
Ensambla todas las imágenes `.png` de `image_folder` (ordenadas alfabéticamente) en un único archivo PDF con fondo blanco y sin canal alfa.
- **Excepciones:** `FileNotFoundError` si la carpeta no existe o no contiene archivos `.png`.

---

### Clase `pdfflatten.utils.Config`

Ubicación: `src/pdfflatten/utils/config.py`

- `Config.BASE_DIR`: `Path.cwd()`
- `Config.RUNTIME_DIR`: `BASE_DIR / "runtime"`
- `Config.PATHS`: `dict[str, Path]` con las rutas de ejecución.
- `Config.ensure_runtime_dirs() -> None`: Crea los directorios `input`, `output`, `processed` y `logs` si no existen.

---

### Función `pdfflatten.utils.setup_logger`

Ubicación: `src/pdfflatten/utils/logger.py`

```python
def setup_logger(
    name: str = "pdfflatten",
    log_file: Path | str | None = None,
    verbose: bool = False,
) -> logging.Logger
```

Configura y devuelve el logger de la aplicación con un `StreamHandler` para consola (`INFO` por defecto, `DEBUG` si `verbose=True`) y un `RotatingFileHandler` para disco (`DEBUG`).
