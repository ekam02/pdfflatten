# 💡 Explicación: ¿Por qué y cómo aplanar un PDF?

Esta sección explica de forma sencilla por qué un documento PDF común puede poner en riesgo tu firma autógrafa o información sensible, y cómo **`pdfflatten`** resuelve este problema.

---

## 🧩 El problema: Un PDF normal es como un "collage de pegatinas"

Cuando creas un documento en Word o en un editor de PDF y le insertas una imagen de tu firma o un sello de tu empresa, el archivo PDF **no funde esos elementos con el papel**.

En realidad, un PDF tradicional guarda cada elemento por separado en **capas independientes**, igual que si pegaras recortes o pegatinas (*stickers*) sobre una hoja:
- El texto va en una capa.
- El logotipo de la empresa va en otra capa.
- **Tu firma va en una capa separada encima del texto.**

### ¿Qué riesgo conlleva esto?
Cualquier persona que reciba ese PDF puede abrirlo con un editor gratuito, hacer clic sobre tu firma, **"despegarla" intacta con fondo transparente** y pegarla en otro documento distinto sin tu autorización. También podría borrar o modificar párrafos del texto original manteniendo tu firma al pie de la página.

---

## 📸 La solución: De "collage" a "fotografía impresa"

El proceso de **aplanar un PDF** (*PDF flattening*) consiste en tomarle una "fotografía digital" a cada página completa y construir un PDF nuevo únicamente con esas fotografías.

```text
   PDF Tradicional (Por capas)              PDF Aplanado (Con pdfflatten)
┌───────────────────────────────┐        ┌───────────────────────────────┐
│  [Capa 3: Imagen de tu firma] │        │                               │
│  [Capa 2: Sello / Anotación]  │  ───►  │   Una sola imagen fija (PNG)  │
│  [Capa 1: Texto seleccionable]│        │   donde todo está fusionado   │
└───────────────────────────────┘        └───────────────────────────────┘
   ⚠️ Se pueden separar las piezas          ✅ Imposible despegar la firma
```

Al pasar tu documento por **`pdfflatten`**:

1. **Se funde todo en una sola capa:** El texto, los sellos y la firma pasan a formar parte de la misma cuadrícula de puntos de color (píxeles).
2. **Tu firma ya no es un objeto separado:** Si alguien intenta extraerla, solo obtendrá la página entera con el texto y las líneas cruzadas detrás, igual que cuando escaneas una hoja de papel firmada a mano.
3. **Se eliminan metadatos y formularios ocultos:** Cualquier comentario, campo editable o capa oculta desaparece porque solo se conserva lo que es visible en la página.

---

## ⚙️ ¿Cómo lo hace `pdfflatten` por dentro?

Sin que tengas que preocuparte por pasos intermedios, la herramienta realiza tres acciones en segundos:

1. **Toma la captura de cada página (*PyMuPDF y Pillow*):** Abre el PDF original y convierte cada página en una imagen PNG de alta nitidez (por defecto a 300 puntos por pulgada).
2. **Usa una carpeta temporal invisible (`tempfile`):** Guarda esas imágenes momentáneamente en una carpeta temporal segura del sistema operativo.
3. **Encuaderna el nuevo PDF y limpia (*Wand / ImageMagick*):** Une todas las imágenes en un nuevo archivo PDF limpio y borra inmediatamente las imágenes temporales para no ocupar espacio ni dejar rastros en tu computadora.

> **⚠️ Nota importante a tener en cuenta:**
> Como el documento final está compuesto por imágenes (igual que un documento escaneado), ya no podrás buscar palabras con `Ctrl + F` ni copiar párrafos de texto del PDF resultante. Por ello, te recomendamos **conservar siempre una copia de tu archivo original** (algo que el modo `--batch` hace automáticamente guardándolo en `runtime/processed/`).
