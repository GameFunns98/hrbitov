import io
import qrcode
from flask import send_file
from weasyprint import HTML


def generate_qr(data):
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf


def generate_pdf(html_content):
    pdf = HTML(string=html_content).write_pdf()
    return io.BytesIO(pdf)
