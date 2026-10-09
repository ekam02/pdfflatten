# Agent Guidelines for pdfflatten

This document outlines the operational rules and standards that AI agents must follow when contributing to the **pdfflatten** repository.

---

## 🎯 Project Overview

- **Name:** `pdfflatten`
- **Purpose:** Converts PDF pages into raster images (PNG) and reassembles them back into a PDF to flatten the document, preventing the unauthorized extraction or manipulation of vector signatures and layers.
- **Stack:** Python 3.8+, PyMuPDF, Wand (ImageMagick), Pillow.

---

## 🛑 Scope of Action & Explicit Authorization (Strict)

AI agents must strictly operate within the boundaries defined by the developer:

1. **Explicit Authorization Required:** Do not create, modify, rename, or delete any files, directories, configurations, or dependencies unless explicitly requested or authorized by the developer.
2. **Proposals Before Implementation:** If improvements, architectural changes, refactors, or new files are identified, propose them in the conversation and wait for developer confirmation before applying any changes.
3. **No Unsolicited Modifications:** Do not perform proactive code edits, refactoring, or file reorganizations outside the exact scope of the current user request.
4. **Clarify Ambiguities:** If a request is open-ended or ambiguous, ask clarifying questions instead of making assumptions or executing actions autonomously.

---

## 📜 Commit Message Rules (Strict)

All commits generated for this repository must strictly adhere to the project's adapted **Conventional Commits** specification:

1. **Language:** Commit messages must be written in **Spanish**.
2. **Imperative Mood:** The first word of the summary must be an **imperative verb** in Spanish (e.g., `agrega`, `corrige`, `refactoriza`, `actualiza`, `elimina`, `añade`, `configura`).
3. **Lowercase First Letter:** The description header following the type prefix must start in **lowercase**. Capitalized verbs are strictly prohibited.

### Format

```text
<type>[optional scope]: <imperative verb in lowercase> <rest of summary>
```

### Allowed Types

- `feat`: New feature or capability.
- `fix`: Bug fix.
- `docs`: Documentation updates only.
- `refactor`: Code refactoring without behavioral change.
- `test`: Adding or updating automated tests.
- `build`: Build system or dependency updates (`pyproject.toml`).
- `ci`: CI/CD workflows and pipelines.
- `chore`: Tooling, configs, or maintenance tasks.
- `style`: Formatting or whitespace fixes without logic changes.
- `perf`: Performance improvements.

### Examples

#### ✅ Valid Examples
- `feat: agrega soporte para configuracion de dpi`
- `fix: corrige lectura de rutas con espacios`
- `docs: actualiza guia de instalacion en el README`
- `refactor(core): reorganiza metodos de conversion de pdf`
- `test: añade pruebas unitarias para rasterizacion`
- `chore: configura reglas de linter`

#### ❌ Invalid Examples
- `feat: Agrega soporte...` *(Violates lowercase rule)*
- `feat: agregado soporte...` *(Past participle instead of imperative)*
- `feat: agregando soporte...` *(Gerund instead of imperative)*
- `feat: add support...` *(English instead of Spanish)*
- `Update README` *(Non-conventional commit format)*

---

## 🧪 Code Quality & Verification Standards

Before committing changes or concluding a task, agents must ensure code quality:

1. **Linting and Formatting:**
   ```bash
   ruff check .
   ruff format --check .
   ```
2. **Type Checking:**
   ```bash
   mypy .
   ```
3. **Automated Testing:**
   ```bash
   pytest
   ```
