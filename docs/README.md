# 📚 Documentación de `pdfflatten`

¡Bienvenido a la guía oficial de **`pdfflatten`**! Esta herramienta te ayuda a **proteger tus documentos PDF** (como contratos, cartas o recibos firmados) convirtiendo cada página en una imagen fija para que nadie pueda despegar tu firma ni alterar el texto original.

Esta documentación está organizada siguiendo el marco **[Diátaxis](https://diataxis.fr/)**, pensado para que encuentres exactamente lo que necesitas según tu nivel de experiencia:

---

## 🧭 ¿Por dónde empezar?

| Cuadrante | ¿Para quién es? | Documento |
| :--- | :--- | :--- |
| 🎓 **1. Tutorial** *(Aprender paso a paso)* | **¿Es tu primera vez aquí o tienes poca experiencia técnica?** Te llevamos de la mano desde cero hasta proteger tu primer PDF. | 👉 **[Primeros pasos con `pdfflatten`](tutorials/primeros-pasos.md)** |
| 🛠️ **2. Guías Prácticas** *(Resolver tareas)* | **¿Ya tienes instalado el programa y quieres hacer algo concreto?** Recetas directas para el día a día. | 👉 **[Cómo procesar varios PDFs, ajustar el tamaño y solucionar problemas](how-to/procesar-varios-pdfs.md)** |
| 💡 **3. Explicación** *(Entender el concepto)* | **¿Quieres saber por qué tu firma corre peligro en un PDF normal y cómo la protegemos?** Explicado sin tecnicismos. | 👉 **[¿Por qué y cómo aplanar un PDF?](explanation/como-funciona-el-aplanado.md)** |
| 📖 **4. Referencia** *(Consulta técnica)* | **¿Buscas la lista exacta de comandos, opciones o funciones de Python?** Diccionario técnico completo. | 👉 **[Referencia del CLI y API interna](reference/cli-y-api.md)** |

---

## ⚡ Resumen Rápido

Si ya tienes todo instalado y solo necesitas recordar el comando básico:

```bash
# Proteger un solo archivo PDF:
pdfflatten mi_documento.pdf -o mi_documento_seguro.pdf

# Proteger automáticamente todos los PDFs de la carpeta runtime/input/:
pdfflatten --batch
```
