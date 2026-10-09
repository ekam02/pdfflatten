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
[ Imágenes PNG por página (dpi configurable) ]
          │
          ▼  (Wand / ImageMagick)
[ Nuevo PDF Reensamblado (Puro mapa de bits) ]
```

1. **Extracción y renderizado:** Renderiza cada página del PDF en una imagen PNG de alta resolución.
2. **Reconstrucción:** Reensambla las imágenes en un nuevo archivo PDF plano, descartando cualquier capa o metadato vectorial previo.

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

## 🛠️ Uso

### Procesamiento por lotes (`main.py`)

Por defecto, el script procesa los archivos depositados en las carpetas de trabajo:

```bash
python main.py
```

* **`docs/input`**: Coloca aquí los archivos PDF a procesar.
* **`docs/output`**: Aquí se generará el PDF final aplanado.
* **`docs/processed`**: Mueve el PDF original una vez procesado.

---

## 🧪 Calidad de Código y Pruebas

El proyecto cuenta con herramientas para garantizar la calidad del código:

* **Linter y formateador (Ruff):**
  ```bash
  ruff check .
  ruff format .
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