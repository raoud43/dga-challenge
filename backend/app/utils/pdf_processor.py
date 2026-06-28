import fitz  # PyMuPDF
from PIL import Image
import io

def convert_pdf_to_images(pdf_bytes, *args, **kwargs):
    """
     Converts each page of a PDF file into a PIL Image using PyMuPDF.
     Modified to accept and ignore any additional variables (such as 'dpi') to prevent errors.
    """
    images = []
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) 
        
        image_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(image_data))
        images.append(image)
        
    pdf_document.close()
    return images