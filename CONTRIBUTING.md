# Guía de Contribución a pdfflatten

¡Gracias por tu interés en contribuir a **pdfflatten**! Toda ayuda es bienvenida para mejorar la herramienta.

Para mantener una base de código limpia y un historial de Git ordenado y fácil de auditar, por favor sigue estas pautas.

---

## 🔀 Flujo de Trabajo

1. **Haz un Fork** del repositorio en GitHub.
2. **Crea una rama descriptiva** para tu cambio:
   ```bash
   git checkout -b feat/soporte-compresion-imagenes
   # o bien:
   git checkout -b fix/corrige-ruta-salida
   ```
3. **Instala el entorno de desarrollo**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```
4. Realiza tus modificaciones y añade pruebas si aplica.
5. Verifica que los tests y análisis estáticos pasen exitosamente.
6. Realiza tus commits siguiendo la convención indicada a continuación.
7. Envía un **Pull Request (PR)** describiendo con claridad los cambios propuestos.

---

## 📝 Convención de Mensajes de Commit (Conventional Commits)

Este proyecto adopta la especificación **[Conventional Commits](https://www.conventionalcommits.org/)** con las siguientes **reglas estrictas**:

1. **Idioma:** Todos los mensajes deben estar redactados en **español**.
2. **Modo verbal imperativo:** El verbo inicial debe estar en imperativo (por ejemplo: *agrega*, *corrige*, *refactoriza*, *actualiza*, *elimina*, *añade*, *configura*).
3. **Minúscula inicial:** La descripción/resumen debe comenzar obligatoriamente en **minúscula**.

### Formato general

```text
<tipo>[alcance opcional]: <verbo imperativo en minúscula> <resto del mensaje>

[cuerpo explicativo opcional]

[pie de página opcional]
```

### Tipos permitidos (`<tipo>`)

| Tipo | Descripción |
| :--- | :--- |
| **`feat`** | Añade una nueva funcionalidad. |
| **`fix`** | Corrige un error o bug. |
| **`docs`** | Modifica únicamente la documentación (`README.md`, docstrings, etc.). |
| **`refactor`** | Reorganiza código sin añadir funciones ni corregir bugs. |
| **`test`** | Añade o modifica pruebas automáticas. |
| **`build`** | Cambios en el empaquetado o dependencias (`pyproject.toml`, etc.). |
| **`ci`** | Cambios en integración continua (GitHub Actions, etc.). |
| **`chore`** | Tareas auxiliares, mantenimiento o herramientas de desarrollo. |
| **`style`** | Ajustes de formato o espacios que no alteran la lógica del código. |
| **`perf`** | Mejoras de rendimiento. |

---

### ✅ Ejemplos Correctos

```text
feat: agrega soporte para configurar dpi desde linea de comandos
fix: corrige excepcion al manejar nombres de archivo con espacios
docs: actualiza guia de instalacion en sistemas debian
refactor: reorganiza logica de conversion a un modulo dedicado
test: añade pruebas unitarias para conversion de imagenes
build: actualiza version minima de pillow en pyproject.toml
chore: configura reglas de linter en configuracion local
```

Con alcance opcional:
```text
feat(cli): añade argumento para definir nivel de compresion
fix(wand): maneja correctamente el canal alfa en fondos transparentes
```

---

### ❌ Ejemplos Incorrectos

* ❌ `feat: Agrega soporte para...` *(Error: inicia con mayúscula).*
* ❌ `feat: agregado soporte para...` *(Error: participio, no es verbo imperativo).*
* ❌ `feat: agregando soporte para...` *(Error: gerundio, no es verbo imperativo).*
* ❌ `feat: add support for...` *(Error: en inglés, debe ser en español).*
* ❌ `arreglado el error` *(Error: no sigue el formato de Conventional Commits).*

---

## 🧪 Verificación de Calidad

Antes de hacer commit y enviar tu PR, asegúrate de que todos los checks pasen sin errores:

```bash
# 1. Linter y formato con Ruff
ruff check .
ruff format --check .

# 2. Comprobación estática de tipos con Mypy
mypy .

# 3. Ejecutar suite de pruebas con Pytest
pytest
```
