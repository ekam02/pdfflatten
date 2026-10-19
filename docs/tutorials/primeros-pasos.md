# 🎓 Tutorial: Primeros pasos con `pdfflatten`

En este tutorial aprenderás, paso a paso y sin necesidad de conocimientos avanzados de programación, cómo instalar **`pdfflatten`** y cómo proteger tu primer documento PDF firmado.

> **⏱️ Tiempo estimado:** 5 minutos.
> **🎯 Objetivo:** Convertir un archivo PDF normal en un PDF "aplanado" (seguro contra copia de firmas).

---

## Paso 1: Preparar tu computadora

`pdfflatten` utiliza dos programas base en tu equipo: **Python** (el lenguaje en que está hecho) e **ImageMagick** (un motor para procesar imágenes).

Si usas **Linux (Ubuntu o Debian)**, abre tu aplicación de **Terminal** y escribe el siguiente comando para asegurarte de tener todo lo necesario:

```bash
sudo apt update && sudo apt install -y python3 python3-venv imagemagick libmagickwand-dev
```

*(Te pedirá la contraseña de tu usuario; escríbela y presiona `Enter`).*

---

## Paso 2: Descargar e instalar `pdfflatten`

1. Entra a la carpeta donde descargaste el proyecto `pdfflatten`:
   ```bash
   cd pdfflatten
   ```

2. Crea un "espacio de trabajo aislado" (llamado entorno virtual) para no mezclar este programa con otros de tu computadora:
   ```bash
   python3 -m venv .venv
   ```

3. Activa ese espacio de trabajo:
   ```bash
   source .venv/bin/activate
   ```
   *(Sabrás que funcionó porque verás `(.venv)` al principio de la línea en tu terminal).*

4. Instala `pdfflatten`:
   ```bash
   pip install -e .
   ```

---

## Paso 3: Comprobar que funciona

Escribe este comando en la terminal y presiona `Enter`:

```bash
pdfflatten --version
```

Si ves en pantalla el siguiente mensaje, ¡la instalación fue un éxito!:

```text
pdfflatten 0.1.0
```

---

## Paso 4: Proteger tu primer documento PDF

Imagina que tienes un archivo llamado `contrato.pdf` al que le pusiste tu firma digitalmente y quieres enviarlo por correo sin que nadie pueda copiar tu firma.

1. Ejecuta el siguiente comando indicando primero tu archivo original y luego, después de `-o` (*output* / salida), el nombre que tendrá el archivo nuevo:

   ```bash
   pdfflatten contrato.pdf -o contrato_seguro.pdf
   ```

2. Verás en pantalla unos mensajes informativos indicando el progreso:

   ```text
   [INFO] Rasterizando PDF 'contrato.pdf' a 300 DPI...
   [INFO] Se generaron 2 imagen(es) desde 'contrato.pdf'.
   [INFO] Ensamblando 2 imagen(es) en 'contrato_seguro.pdf'...
   [INFO] PDF aplanado guardado exitosamente en 'contrato_seguro.pdf'.
   ```

3. **¡Listo!** Abre `contrato_seguro.pdf` con tu visor de PDF habitual.
   - Verás que luce exactamente igual que el original.
   - Sin embargo, si intentas seleccionar el texto con el ratón o hacer clic sobre tu firma para arrastrarla o copiarla, notarás que **ya no es posible**: toda la página es ahora una única imagen indivisible.

---

## 🎉 ¿Qué sigue?

- ¿Tienes muchos PDFs que proteger al mismo tiempo? Revisa las **[Guías Prácticas (How-To)](../how-to/procesar-varios-pdfs.md)**.
- ¿Tienes curiosidad por entender cómo funciona esta protección por dentro? Lee la **[Explicación conceptual](../explanation/como-funciona-el-aplanado.md)**.
