



from pdf2image import convert_from_bytes
from typing import List
from PIL import Image

def convert_pdf_to_images(pdf_bytes: bytes, dpi: int = 150) -> List[Image.Image]:
    """
    تحويل ملف PDF ممرر كـ bytes إلى قائمة من صور PIL في الذاكرة.
    """
    try:
        images = convert_from_bytes(pdf_bytes, dpi=dpi)
        return images
    except Exception as e:
        raise RuntimeError(f"فشل معالج الـ PDF في تحويل الملف إلى صور: {str(e)}")