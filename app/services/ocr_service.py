# app/services/ocr_service.py

import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import io

class OCRService:
    def __init__(self, lang: str = "eng"):
        self.lang = lang

    def extract_text(self, file_bytes: bytes, filename: str) -> str:
        if filename.lower().endswith(".pdf"):
            return self._extract_from_pdf(file_bytes)
        else:
            return self._extract_from_image(file_bytes)

    def _extract_from_image(self, file_bytes: bytes) -> str:
        image = Image.open(io.BytesIO(file_bytes))
        return pytesseract.image_to_string(image, lang=self.lang)

    def _extract_from_pdf(self, file_bytes: bytes) -> str:
        text = ""
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
        return text
