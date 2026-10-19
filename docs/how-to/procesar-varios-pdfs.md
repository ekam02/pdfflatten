# 🛠️ Guías Prácticas (How-To)

Estas guías responden a preguntas concretas del día a día. Úsalas como recetas rápidas cuando tengas un objetivo específico.

---

## 1. Cómo procesar muchos archivos PDF a la vez (Modo por lotes)

Si tienes decenas de documentos por proteger, no necesitas escribir un comando por cada archivo.

### Pasos:

1. Ejecuta una vez el modo por lotes para que `pdfflatten` cree las carpetas de trabajo automáticamente:
   ```bash
   pdfflatten --batch
   ```
2. Verás que dentro del proyecto existe una carpeta llamada `runtime/` con tres subcarpetas:
   - 📂 **`runtime/input/`**: Copia o arrastra aquí todos los PDFs que quieras proteger.
   - 📂 **`runtime/output/`**: Aquí aparecerán tus PDFs ya protegidos (aplanados).
   - 📂 **`runtime/processed/`**: Aquí se guardarán automáticamente tus PDFs originales una vez terminados, para que no se procesen dos veces por error.
3. Cuando hayas copiado tus archivos en `runtime/input/`, vuelve a ejecutar:
   ```bash
   pdfflatten --batch
   ```
4. Recoge tus documentos listos en **`runtime/output/`**.

> **💡 Consejo:** Si tus archivos están en otra carpeta de tu computadora (por ejemplo, en el Escritorio), puedes indicársela directamente sin moverlos a `runtime/`:
> ```bash
> pdfflatten --batch --input-dir ~/Escritorio/por_firmar --output-dir ~/Escritorio/listos
> ```

---

## 2. Cómo reducir el peso (tamaño en MB) del PDF generado

Al convertir páginas en imágenes de alta calidad, el archivo resultante puede pesar más que el original. Puedes controlar el equilibrio entre **nitidez** y **peso del archivo** con la opción `--dpi` (puntos por pulgada):

- **Para enviar por correo electrónico o WhatsApp (archivo ligero):** Usa `150` DPI.
  ```bash
  pdfflatten documento.pdf -o documento_ligero.pdf --dpi 150
  ```
- **Uso estándar de oficina (balance ideal, valor por defecto):** Usa `300` DPI.
  ```bash
  pdfflatten documento.pdf -o documento_estandar.pdf --dpi 300
  ```
- **Para impresión física de alta precisión:** Usa `400` o `600` DPI.
  ```bash
  pdfflatten documento.pdf -o documento_impresion.pdf --dpi 400
  ```

---

## 3. Cómo solucionar el error de permisos de ImageMagick en Linux (`policy.xml`)

En algunas versiones de Ubuntu o Debian, el programa ImageMagick bloquea por defecto la creación de archivos PDF por políticas del sistema y muestra un error similar a `not authorized @ error/constitute.c/WriteImage`.

### Cómo resolverlo:

1. Abre el archivo de configuración de ImageMagick con permisos de administrador:
   ```bash
   sudo nano /etc/ImageMagick-6/policy.xml
   ```
   *(Si tienes ImageMagick 7, la ruta suele ser `/etc/ImageMagick-7/policy.xml`).*

2. Busca cerca del final del archivo la siguiente línea:
   ```xml
   <policy domain="coder" rights="none" pattern="PDF" />
   ```

3. Cambia la palabra `none` por `read|write` para que quede así:
   ```xml
   <policy domain="coder" rights="read|write" pattern="PDF" />
   ```

4. Guarda los cambios (`Ctrl + O`, luego `Enter`) y cierra el editor (`Ctrl + X`). Vuelve a ejecutar `pdfflatten`.

---

## 4. Cómo ver el registro detallado si algo falla

Si un documento da error y necesitas saber qué ocurrió exactamente:

1. Agrega la opción `--verbose` (o `-v`) a tu comando para ver todos los detalles en pantalla:
   ```bash
   pdfflatten archivo_con_problemas.pdf --verbose
   ```
2. Además, todos los eventos quedan guardados automáticamente en el archivo de historial:
   ```text
   runtime/logs/app.log
   ```
