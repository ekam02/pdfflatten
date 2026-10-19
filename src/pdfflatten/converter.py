from __future__ import annotations

import logging
import tempfile
from pathlib import Path

import pymupdf
from PIL import Image
from wand.color import Color  # type: ignore[import-untyped]
from wand.image import Image as WandImage  # type: ignore[import-untyped]

logger = logging.getLogger("pdfflatten")


class Converter:
    """Núcleo de conversión para rasterizar páginas PDF a PNG y reensamblarlas en un nuevo PDF."""

    @staticmethod
    def convert_pdf_to_images(
        pdf_path: Path | str,
        output_folder: Path | str,
        dpi: int = 300,
    ) -> list[Path]:
        """Convierte las páginas de un documento PDF en imágenes PNG individuales.

        Args:
            pdf_path: Ruta al archivo PDF de origen.
            output_folder: Carpeta destino donde se guardarán las imágenes PNG.
            dpi: Resolución de rasterizado en puntos por pulgada (defecto: 300).

        Returns:
            Lista ordenada de rutas (`Path`) a las imágenes PNG generadas.

        Raises:
            FileNotFoundError: Si el archivo PDF de origen no existe.
            ValueError: Si el valor de DPI no es positivo.
        """
        if dpi <= 0:
            raise ValueError(f"El valor de DPI debe ser mayor que 0 (recibido: {dpi}).")

        src_path = Path(pdf_path)
        if not src_path.is_file():
            logger.error("Archivo PDF no encontrado: %s", src_path)
            raise FileNotFoundError(f"No se encontró el archivo PDF: {src_path}")

        out_dir = Path(output_folder)
        out_dir.mkdir(parents=True, exist_ok=True)

        logger.info("Rasterizando PDF '%s' a %d DPI...", src_path.name, dpi)
        generated_images: list[Path] = []

        doc = pymupdf.open(str(src_path))
        try:
            total_pages = len(doc)
            logger.debug(
                "Documento '%s' abierto con %d página(s).", src_path.name, total_pages
            )
            for i in range(total_pages):
                page = doc[i]
                pix = page.get_pixmap(dpi=dpi)
                image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                img_path = out_dir / f"page_{i + 1:04d}.png"
                image.save(str(img_path), dpi=(dpi, dpi))
                generated_images.append(img_path)
                logger.debug(
                    "Página %d/%d guardada en '%s'.", i + 1, total_pages, img_path
                )
        finally:
            doc.close()

        logger.info(
            "Se generaron %d imagen(es) desde '%s'.",
            len(generated_images),
            src_path.name,
        )
        return generated_images

    @staticmethod
    def convert_images_to_pdf(
        image_folder: Path | str,
        output_pdf_path: Path | str,
    ) -> Path:
        """Reensambla las imágenes PNG de una carpeta en un único archivo PDF plano.

        Args:
            image_folder: Carpeta que contiene las imágenes a ensamblar.
            output_pdf_path: Ruta del archivo PDF de salida.

        Returns:
            Ruta (`Path`) al archivo PDF generado.

        Raises:
            FileNotFoundError: Si la carpeta no existe o no contiene imágenes.
        """
        folder_path = Path(image_folder)
        if not folder_path.is_dir():
            logger.error("Carpeta de imágenes no encontrada: %s", folder_path)
            raise FileNotFoundError(
                f"No existe el directorio de imágenes: {folder_path}"
            )

        image_files = sorted(
            p
            for p in folder_path.iterdir()
            if p.is_file() and p.suffix.lower() == ".png"
        )
        if not image_files:
            logger.error("No se encontraron imágenes PNG en: %s", folder_path)
            raise FileNotFoundError(f"No se encontraron imágenes PNG en: {folder_path}")

        dest_path = Path(output_pdf_path)
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Ensamblando %d imagen(es) en '%s'...", len(image_files), dest_path)
        with WandImage() as pdf:
            for image_path in image_files:
                logger.debug(
                    "Agregando imagen '%s' a la secuencia PDF.", image_path.name
                )
                with WandImage(filename=str(image_path)) as img:
                    img.background_color = Color("white")
                    img.alpha_channel = "remove"
                    img.format = "pdf"
                    pdf.sequence.append(img)

            pdf.save(filename=str(dest_path))

        logger.info("PDF aplanado guardado exitosamente en '%s'.", dest_path)
        return dest_path

    @classmethod
    def flatten_pdf(
        cls,
        input_pdf: Path | str,
        output_pdf: Path | str,
        dpi: int = 300,
    ) -> Path:
        """Aplana un archivo PDF convirtiéndolo a imágenes en un directorio temporal y reensamblándolo.

        Args:
            input_pdf: Ruta del archivo PDF de entrada.
            output_pdf: Ruta del archivo PDF de salida.
            dpi: Resolución de rasterizado en puntos por pulgada (defecto: 300).

        Returns:
            Ruta (`Path`) del archivo PDF final aplanado.
        """
        src_path = Path(input_pdf)
        dest_path = Path(output_pdf)
        logger.debug(
            "Iniciando aplanado de '%s' -> '%s' (DPI=%d).",
            src_path,
            dest_path,
            dpi,
        )
        with tempfile.TemporaryDirectory(prefix="pdfflatten_") as tmp_dir:
            logger.debug("Directorio temporal creado: %s", tmp_dir)
            cls.convert_pdf_to_images(src_path, tmp_dir, dpi=dpi)
            result = cls.convert_images_to_pdf(tmp_dir, dest_path)
        logger.debug(
            "Directorio temporal eliminado tras completar '%s'.", dest_path.name
        )
        return result
