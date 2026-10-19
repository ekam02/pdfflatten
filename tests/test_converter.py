from __future__ import annotations

from pathlib import Path

import pymupdf
import pytest

from pdfflatten.converter import Converter


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    """Crea un archivo PDF de prueba con 2 páginas y texto vectorial."""
    pdf_path = tmp_path / "sample.pdf"
    doc = pymupdf.open()
    for i in range(2):
        page = doc.new_page(width=200, height=200)
        page.insert_text((20, 50), f"Pagina de prueba {i + 1}")
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


def test_convert_pdf_to_images_creates_pngs(sample_pdf: Path, tmp_path: Path) -> None:
    out_dir = tmp_path / "images"
    out_dir.mkdir()

    image_paths = Converter.convert_pdf_to_images(sample_pdf, out_dir, dpi=150)

    assert len(image_paths) == 2
    for img_path in image_paths:
        assert img_path.is_file()
        assert img_path.suffix == ".png"


def test_convert_pdf_to_images_missing_file_raises(tmp_path: Path) -> None:
    missing_pdf = tmp_path / "no_existe.pdf"
    out_dir = tmp_path / "images"
    out_dir.mkdir()

    with pytest.raises(FileNotFoundError):
        Converter.convert_pdf_to_images(missing_pdf, out_dir)


def test_convert_images_to_pdf_creates_valid_pdf(
    sample_pdf: Path, tmp_path: Path
) -> None:
    img_dir = tmp_path / "images"
    img_dir.mkdir()
    out_pdf = tmp_path / "output" / "result.pdf"

    Converter.convert_pdf_to_images(sample_pdf, img_dir, dpi=100)
    result_path = Converter.convert_images_to_pdf(img_dir, out_pdf)

    assert result_path == out_pdf
    assert out_pdf.is_file()
    with pymupdf.open(str(out_pdf)) as doc:
        assert len(doc) == 2


def test_flatten_pdf_uses_tempdir_and_cleans_up(
    sample_pdf: Path, tmp_path: Path
) -> None:
    out_pdf = tmp_path / "flattened" / "output.pdf"

    result = Converter.flatten_pdf(sample_pdf, out_pdf, dpi=150)

    assert result == out_pdf
    assert out_pdf.is_file()
    with pymupdf.open(str(out_pdf)) as doc:
        assert len(doc) == 2
        # El PDF aplanado no debe contener texto seleccionable vectorial
        assert doc[0].get_text().strip() == ""


def test_convert_pdf_to_images_invalid_dpi_raises(
    sample_pdf: Path, tmp_path: Path
) -> None:
    with pytest.raises(ValueError, match="DPI"):
        Converter.convert_pdf_to_images(sample_pdf, tmp_path, dpi=0)


def test_convert_images_to_pdf_empty_or_missing_folder_raises(tmp_path: Path) -> None:
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    out_pdf = tmp_path / "out.pdf"

    with pytest.raises(FileNotFoundError):
        Converter.convert_images_to_pdf(empty_dir, out_pdf)

    with pytest.raises(FileNotFoundError):
        Converter.convert_images_to_pdf(tmp_path / "nonexistent", out_pdf)
