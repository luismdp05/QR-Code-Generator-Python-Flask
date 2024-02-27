from flask import Flask, render_template, request
import qrcode
from PIL import Image
import os
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
    
    # Generar un nombre de archivo único
    timestamp = int(time.time())
    filename = f'qr_code_{timestamp}.png'
    img_path = os.path.join('static', filename)
    img.save(img_path)

    # Retornar la ruta del archivo guardado
    return render_template('index.html', qr_img=img_path)

if __name__ == '__main__':
    app.run(debug=True)
