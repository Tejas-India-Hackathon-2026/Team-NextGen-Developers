import io
import pypdf

def scan_pdf_binary(file_bytes: bytes, selected_subject: str, title: str) -> tuple:
    if len(file_bytes) < 1024:
        return False, 'File is virtually empty (< 1 KB).', {}
    if not file_bytes.startswith(b'%PDF-') and b'%PDF-' not in file_bytes[:1024]:
        return False, 'Invalid binary format: missing %PDF- header.', {}
    try:
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        if len(reader.pages) == 0:
            return False, 'PDF contains 0 pages.', {}
        return True, 'Valid', {'pages': len(reader.pages), 'quality_score': 90}
    except Exception as e:
        return False, str(e), {}
