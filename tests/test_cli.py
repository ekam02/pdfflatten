from __future__ import annotations

from pathlib import Path

import pymupdf
import pytest

from pdfflatten import __version__
from pdfflatten.cli import main
from pdfflatten.utils.config import Config


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    pdf_path = tmp_path / "doc.pdf"
    doc = pymupdf.open()
    page = doc.new_page(width=200, height=200)
    page.insert_text((20, 50), "Contenido vectorial")
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


@pytest.fixture(autouse=True)
def isolated_runtime(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> dict[str, Path]:
    runtime_dir = tmp_path / "runtime"
    paths = {
        "input": runtime_dir / "input",
        "output": runtime_dir / "output",
        "processed": runtime_dir / "processed",
        "logs": runtime_dir / "logs",
        "app_log": runtime_dir / "logs" / "app.log",
    }
    monkeypatch.setattr(Config, "RUNTIME_DIR", runtime_dir)
    monkeypatch.setattr(Config, "PATHS", paths)
    return paths


def test_cli_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert __version__ in captured.out


def test_cli_no_arguments_returns_error() -> None:
    exit_code = main([])
    assert exit_code == 1


def test_cli_single_file_conversion(sample_pdf: Path, tmp_path: Path) -> None:
    output_pdf = tmp_path / "salida.pdf"
    exit_code = main([str(sample_pdf), "-o", str(output_pdf), "--dpi", "120"])

    assert exit_code == 0
    assert output_pdf.is_file()
    with pymupdf.open(str(output_pdf)) as doc:
        assert len(doc) == 1


def test_cli_single_file_default_output(
    sample_pdf: Path, isolated_runtime: dict[str, Path]
) -> None:
    exit_code = main([str(sample_pdf), "--dpi", "100", "--verbose"])

    assert exit_code == 0
    expected_out = isolated_runtime["output"] / sample_pdf.name
    assert expected_out.is_file()


def test_cli_single_file_missing_returns_error(tmp_path: Path) -> None:
    missing = tmp_path / "inexistente.pdf"
    exit_code = main([str(missing)])
    assert exit_code == 1


def test_cli_invalid_dpi_returns_error(sample_pdf: Path) -> None:
    exit_code = main([str(sample_pdf), "--dpi", "0"])
    assert exit_code == 1


def test_cli_batch_mode_processes_and_archives_pdfs(
    sample_pdf: Path, isolated_runtime: dict[str, Path]
) -> None:
    input_dir = isolated_runtime["input"]
    output_dir = isolated_runtime["output"]
    processed_dir = isolated_runtime["processed"]
    input_dir.mkdir(parents=True, exist_ok=True)

    pdf1 = input_dir / "uno.pdf"
    pdf2 = input_dir / "dos.pdf"
    pdf1.write_bytes(sample_pdf.read_bytes())
    pdf2.write_bytes(sample_pdf.read_bytes())

    exit_code = main(
        [
            "--batch",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--dpi",
            "100",
        ]
    )

    assert exit_code == 0
    assert (output_dir / "uno.pdf").is_file()
    assert (output_dir / "dos.pdf").is_file()
    assert (processed_dir / "uno.pdf").is_file()
    assert (processed_dir / "dos.pdf").is_file()
    assert not pdf1.exists()
    assert not pdf2.exists()


def test_cli_batch_mode_empty_directory(isolated_runtime: dict[str, Path]) -> None:
    exit_code = main(["--batch"])
    assert exit_code == 0


def test_cli_single_file_output_to_directory(sample_pdf: Path, tmp_path: Path) -> None:
    dest_dir = tmp_path / "custom_out"
    dest_dir.mkdir()
    exit_code = main([str(sample_pdf), "-o", str(dest_dir), "--dpi", "100"])

    assert exit_code == 0
    assert (dest_dir / sample_pdf.name).is_file()


def test_cli_batch_mode_corrupted_pdf_returns_error(
    isolated_runtime: dict[str, Path],
) -> None:
    input_dir = isolated_runtime["input"]
    input_dir.mkdir(parents=True, exist_ok=True)
    bad_pdf = input_dir / "corrupto.pdf"
    bad_pdf.write_text("no es un pdf valido", encoding="utf-8")

    exit_code = main(["--batch"])
    assert exit_code == 1
