from __future__ import annotations

import argparse
import logging
import shutil
from collections.abc import Sequence
from pathlib import Path

from wand.exceptions import WandException  # type: ignore[import-untyped]

from pdfflatten import __version__
from pdfflatten.converter import Converter
from pdfflatten.utils.config import Config
from pdfflatten.utils.logger import setup_logger


def build_parser() -> argparse.ArgumentParser:
    """Construye y devuelve el parser de argumentos del CLI."""
    parser = argparse.ArgumentParser(
        prog="pdfflatten",
        description=(
            "Convierte y aplana documentos PDF rasterizando cada página en imágenes "
            "para prevenir la extracción o manipulación de firmas y capas vectoriales."
        ),
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        help="Ruta del archivo PDF individual a procesar (opcional si se usa --batch).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Ruta del archivo PDF de salida o directorio destino.",
    )
    parser.add_argument(
        "-b",
        "--batch",
        action="store_true",
        help="Procesa todos los archivos PDF en el directorio de entrada.",
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=None,
        help="Directorio de entrada para el modo --batch (por defecto: runtime/input).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directorio de salida para el modo --batch (por defecto: runtime/output).",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=None,
        help="Directorio donde se archivan los PDFs procesados en modo --batch (por defecto: runtime/processed).",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Resolución de rasterizado en puntos por pulgada (por defecto: 300).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Activa el nivel de detalle DEBUG en la salida de consola.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Muestra la versión actual de la herramienta.",
    )
    return parser


def _resolve_single_output(input_path: Path, output_arg: Path | None) -> Path:
    """Resuelve la ruta de archivo de salida para el procesamiento individual."""
    if output_arg is None:
        Config.PATHS["output"].mkdir(parents=True, exist_ok=True)
        return Config.PATHS["output"] / input_path.name

    if output_arg.is_dir():
        return output_arg / input_path.name

    return output_arg


def _run_batch(
    input_dir: Path,
    output_dir: Path,
    processed_dir: Path,
    dpi: int,
) -> int:
    """Ejecuta el procesamiento por lotes sobre todos los PDFs en input_dir."""
    logger = logging.getLogger("pdfflatten")

    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(
        p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"
    )

    if not pdf_files:
        logger.info("No se encontraron archivos PDF para procesar en '%s'.", input_dir)
        return 0

    logger.info("Iniciando procesamiento por lotes de %d archivo(s)...", len(pdf_files))
    errors = 0
    for pdf_file in pdf_files:
        dest_pdf = output_dir / pdf_file.name
        archived_pdf = processed_dir / pdf_file.name
        try:
            Converter.flatten_pdf(pdf_file, dest_pdf, dpi=dpi)
            shutil.move(str(pdf_file), str(archived_pdf))
            logger.info("Original archivado en '%s'.", archived_pdf)
        except (OSError, ValueError, RuntimeError, WandException) as exc:
            logger.error("Error al procesar '%s': %s", pdf_file, exc)
            errors += 1

    if errors > 0:
        logger.error("Procesamiento por lotes finalizado con %d error(es).", errors)
        return 1

    logger.info("Procesamiento por lotes completado con éxito.")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada principal de la interfaz de línea de comandos."""
    parser = build_parser()
    args = parser.parse_args(argv)

    Config.ensure_runtime_dirs()
    logger = setup_logger(
        name="pdfflatten",
        log_file=Config.PATHS["app_log"],
        verbose=args.verbose,
    )

    if args.dpi <= 0:
        logger.error(
            "El parámetro --dpi debe ser un entero mayor que 0 (recibido: %d).",
            args.dpi,
        )
        return 1

    if not args.batch and args.path is None:
        parser.print_help()
        logger.error(
            "Debe especificar la ruta de un archivo PDF o utilizar el modo --batch."
        )
        return 1

    if args.batch:
        in_dir: Path = (
            args.input_dir if args.input_dir is not None else Config.PATHS["input"]
        )
        out_dir: Path = (
            args.output_dir if args.output_dir is not None else Config.PATHS["output"]
        )
        proc_dir: Path = (
            args.processed_dir
            if args.processed_dir is not None
            else Config.PATHS["processed"]
        )
        return _run_batch(in_dir, out_dir, proc_dir, dpi=args.dpi)

    input_path: Path = args.path
    output_path = _resolve_single_output(input_path, args.output)

    try:
        Converter.flatten_pdf(input_path, output_path, dpi=args.dpi)
    except (OSError, ValueError, RuntimeError, WandException) as exc:
        logger.error("Fallo al procesar '%s': %s", input_path, exc)
        return 1

    return 0
