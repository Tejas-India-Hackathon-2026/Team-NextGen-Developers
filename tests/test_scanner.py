import io, pypdf
from modules.scanner import scan_pdf_binary

def test_bad_header():
    ok, msg, _ = scan_pdf_binary(b'Not a pdf', 'Python', 'Title')
    assert ok is False

def test_good_pdf():
    w = pypdf.PdfWriter()
    w.add_blank_page(width=100, height=100)
    buf = io.BytesIO()
    w.write(buf)
    ok, _, summary = scan_pdf_binary(buf.getvalue(), 'Python', 'Python Notes')
    assert ok is True
    assert summary['pages'] == 1
