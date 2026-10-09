from fitz import fitz
import os
from PIL import Image
from wand.image import Image as WandImage
from wand.color import Color


class Converter:
    def __init__(self):
        pass

    @staticmethod
    def convert_pdf_to_images(pdf_path, output_folder, dpi=200):
        doc = fitz.open(pdf_path)

        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=dpi)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            image.save(f"{output_folder}/page_{i + 1}.png", dpi=(dpi, dpi))

        doc.close()

    @staticmethod
    def convert_images_to_pdf(image_folder, output_pdf_path):
        image_files = sorted(os.listdir(image_folder))

        with WandImage() as pdf:
            for image_file in image_files:
                image_path = os.path.join(image_folder, image_file)
                with WandImage(filename=image_path) as img:
                    img.background_color = Color("white")
                    img.alpha_channel = 'remove'
                    img.format = 'pdf'
                    pdf.sequence.append(img)

            pdf.save(filename=output_pdf_path)
