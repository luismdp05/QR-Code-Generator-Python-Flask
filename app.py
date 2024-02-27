from flask import Flask, render_template, request, url_for
import qrcode
from PIL import Image
import os
import uuid
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.form.get('data')

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Generar un nombre de archivo único con el formato QR-Code_
    unique_id = uuid.uuid4().hex
    filename = f'QR-Code_{unique_id}.png'
    
    # Asegurarse de que la carpeta 'static/qr-result' exista
    if not os.path.exists('static/qr-result'):
        os.makedirs('static/qr-result')
    
    img_path = os.path.join('static/qr-result', filename)
    img.save(img_path)

    # Generar la URL accesible para la imagen del código QR
    qr_img_url = url_for('static', filename=f'qr-result/{filename}')

    # Retornar la ruta del archivo guardado
    return render_template('index.html', qr_img=qr_img_url)

if __name__ == '__main__':
    app.run(debug=True)
