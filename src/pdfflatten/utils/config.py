from __future__ import annotations

from pathlib import Path
from typing import ClassVar


class Config:
    """Configuración centralizada de rutas de trabajo en runtime/."""

    BASE_DIR: ClassVar[Path] = Path.cwd()
    RUNTIME_DIR: ClassVar[Path] = BASE_DIR / "runtime"

    PATHS: ClassVar[dict[str, Path]] = {
        "input": RUNTIME_DIR / "input",
        "output": RUNTIME_DIR / "output",
        "processed": RUNTIME_DIR / "processed",
        "logs": RUNTIME_DIR / "logs",
        "app_log": RUNTIME_DIR / "logs" / "app.log",
    }

    @classmethod
    def ensure_runtime_dirs(cls) -> None:
        """Garantiza que los directorios de runtime/ existan."""
        for key in ("input", "output", "processed", "logs"):
            cls.PATHS[key].mkdir(parents=True, exist_ok=True)
