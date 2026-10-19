# pdfflatten

> Convierte y aplana documentos PDF rasterizando cada página en imágenes para proteger firmas y prevenir la manipulación de capas vectoriales.

---

## 💡 Motivación

Al firmar documentos digitalmente insertando una imagen de firma o trazo, muchos editores de PDF conservan la firma como un objeto independiente o capa vectorial. Esto facilita que terceros puedan extraer la firma en alta resolución o manipular el contenido del documento.

**`pdfflatten`** mitiga este riesgo transformando cada página del documento PDF en una imagen fija (PNG) y recomponiendo posteriormente un nuevo PDF a partir de dichas imágenes. Al hacer esto:

- **Se aplana el documento (*flattening*):** Todo el contenido vectorial, texto y firmas pasan a ser una sola matriz de píxeles por página.
- **Se elimina la extracción de elementos individuales:** Resulta imposible seleccionar o copiar la firma como capa independiente o vector limpio.
- **Se eliminan formularios o anotaciones interactivas ocultas.**

---

## ⚙️ ¿Cómo funciona?

```text
[ Documento PDF Original ]
          │
          ▼  (PyMuPDF / Pillow)
[ Imágenes PNG temporales por página (DPI configurable) ]
          │
          ▼  (Wand / ImageMagick)
[ Nuevo PDF Reensamblado (Puro mapa de bits) ]
```

1. **Extracción y renderizado:** Renderiza cada página del PDF en una imagen PNG dentro de un directorio temporal aislado (`tempfile.TemporaryDirectory`).
2. **Reconstrucción:** Reensambla las imágenes en un nuevo archivo PDF plano, descartando cualquier capa o metadato vectorial previo y limpiando automáticamente los archivos temporales.

---

## 📋 Requisitos del Sistema

Además de Python (>= 3.8), este proyecto utiliza [Wand](https://docs.wand-py.org/), el cual requiere tener instalado **ImageMagick** en el sistema operativo:

### Linux (Debian / Ubuntu)
```bash
sudo apt install imagemagick libmagickwand-dev
```

*(Nota: En algunas distribuciones puede ser necesario ajustar `/etc/ImageMagick-6/policy.xml` para permitir operaciones de lectura/escritura en PDFs).*

---

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/pdfflatten.git
   cd pdfflatten
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instala el paquete junto con las dependencias de desarrollo:
   ```bash
   pip install -e ".[dev]"
   ```

---

## 🛠️ Uso (CLI)

Una vez instalado el paquete, puedes ejecutar el comando `pdfflatten` directamente o mediante `python -m pdfflatten`:

### 1. Modo de archivo individual

```bash
# Aplanar un PDF especificando ruta de salida y resolución
pdfflatten documento.pdf -o documento_aplanado.pdf --dpi 300

# Aplanar un PDF hacia el directorio por defecto (runtime/output/documento.pdf)
pdfflatten documento.pdf
```

### 2. Modo de procesamiento por lotes (`--batch`)

Procesa todos los archivos PDF ubicados en el directorio de entrada (`runtime/input` por defecto), genera los PDFs aplanados en `runtime/output` y archiva los originales en `runtime/processed`:

```bash
# Usando las carpetas de runtime/ por defecto
pdfflatten --batch

# Especificando directorios personalizados y modo detallado
pdfflatten --batch --input-dir ./entradas --output-dir ./salidas --dpi 200 --verbose
```

### 3. Opciones disponibles

| Argumento / Flag | Descripción |
| :--- | :--- |
| `path` | Ruta del archivo PDF individual a procesar. |
| `-o, --output` | Ruta del archivo PDF de salida o directorio destino. |
| `-b, --batch` | Procesa todos los archivos PDF en el directorio de entrada. |
| `--input-dir` | Directorio de entrada para `--batch` (defecto: `runtime/input`). |
| `--output-dir` | Directorio de salida para `--batch` (defecto: `runtime/output`). |
| `--processed-dir` | Directorio donde se archivan los originales en `--batch` (defecto: `runtime/processed`). |
| `--dpi` | Resolución de rasterizado en puntos por pulgada (defecto: `300`). |
| `-v, --verbose` | Muestra mensajes de nivel `DEBUG` en consola. |
| `-V, --version` | Muestra la versión instalada de la herramienta. |

---

## 📚 Documentación (Estructura Diátaxis)

La documentación en [`docs/`](docs/README.md) está organizada con el marco **Diátaxis** para adaptarse tanto a usuarios sin experiencia técnica como a desarrolladores:

- 🧭 **[Índice General de Documentación](docs/README.md)**
- 🎓 **[Tutorial: Primeros pasos paso a paso](docs/tutorials/primeros-pasos.md)** *(Ideal para nuevos usuarios)*
- 🛠️ **[Guías Prácticas (How-To): Procesar por lotes, ajustar peso y resolver errores](docs/how-to/procesar-varios-pdfs.md)**
- 💡 **[Explicación: ¿Por qué y cómo aplanar un PDF?](docs/explanation/como-funciona-el-aplanado.md)** *(Sin tecnicismos)*
- 📖 **[Referencia Técnica: CLI y API de Python](docs/reference/cli-y-api.md)**

---

## 🧪 Calidad de Código y Pruebas

El proyecto cuenta con herramientas para garantizar la calidad del código:

* **Linter y formateador (Ruff):**
  ```bash
  ruff check .
  ruff format --check .
  ```

* **Chequeo de tipos (Mypy):**
  ```bash
  mypy .
  ```

* **Pruebas unitarias (Pytest):**
  ```bash
  pytest
  ```

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si deseas colaborar, por favor consulta la [Guía de Contribución](CONTRIBUTING.md) para conocer las pautas de estilo, flujo de trabajo y la convención de commits (*Conventional Commits* en español e imperativo en minúsculas).

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.