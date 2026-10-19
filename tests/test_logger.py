import logging
from pathlib import Path

from pdfflatten.utils.config import Config
from pdfflatten.utils.logger import setup_logger


def test_config_paths_are_pathlib_objects() -> None:
    assert isinstance(Config.BASE_DIR, Path)
    assert isinstance(Config.RUNTIME_DIR, Path)
    for key in ("input", "output", "processed", "logs", "app_log"):
        assert key in Config.PATHS
        assert isinstance(Config.PATHS[key], Path)


def test_config_ensure_runtime_dirs(tmp_path: Path, monkeypatch: object) -> None:
    runtime_dir = tmp_path / "runtime"
    paths = {
        "input": runtime_dir / "input",
        "output": runtime_dir / "output",
        "processed": runtime_dir / "processed",
        "logs": runtime_dir / "logs",
        "app_log": runtime_dir / "logs" / "app.log",
    }
    monkeypatch.setattr(Config, "RUNTIME_DIR", runtime_dir)  # type: ignore[attr-defined]
    monkeypatch.setattr(Config, "PATHS", paths)  # type: ignore[attr-defined]

    Config.ensure_runtime_dirs()

    assert paths["input"].is_dir()
    assert paths["output"].is_dir()
    assert paths["processed"].is_dir()
    assert paths["logs"].is_dir()


def test_setup_logger_creates_log_file_and_logs_messages(tmp_path: Path) -> None:
    log_file = tmp_path / "logs" / "app.log"
    logger = setup_logger(
        name="test_pdfflatten_default", log_file=log_file, verbose=False
    )

    assert log_file.parent.is_dir()
    logger.debug("mensaje debug oculto en consola pero visible en archivo")
    logger.info("mensaje info")

    for handler in logger.handlers:
        handler.flush()

    assert log_file.is_file()
    content = log_file.read_text(encoding="utf-8")
    assert "mensaje debug oculto en consola pero visible en archivo" in content
    assert "mensaje info" in content
    assert "[DEBUG]" in content
    assert "[INFO]" in content


def test_setup_logger_verbose_sets_console_debug(tmp_path: Path) -> None:
    log_file = tmp_path / "logs" / "verbose.log"
    logger_normal = setup_logger(name="test_normal", log_file=log_file, verbose=False)
    stream_handlers_normal = [
        h
        for h in logger_normal.handlers
        if isinstance(h, logging.StreamHandler)
        and not isinstance(h, logging.FileHandler)
    ]
    assert len(stream_handlers_normal) == 1
    assert stream_handlers_normal[0].level == logging.INFO

    logger_verbose = setup_logger(name="test_verbose", log_file=log_file, verbose=True)
    stream_handlers_verbose = [
        h
        for h in logger_verbose.handlers
        if isinstance(h, logging.StreamHandler)
        and not isinstance(h, logging.FileHandler)
    ]
    assert len(stream_handlers_verbose) == 1
    assert stream_handlers_verbose[0].level == logging.DEBUG
