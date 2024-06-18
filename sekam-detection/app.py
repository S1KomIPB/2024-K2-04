# app.py
from flask import Flask, request, render_template, redirect, url_for
import cv2
import numpy as np
import joblib
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Memuat model
model = joblib.load('model/pnn_model.pkl')

# Data tabel lignin
data_tabel = [
    {"kelas": 0, "sekam": 0, "dedak": 10, "lignin": 10.19},
    {"kelas": 1, "sekam": 1, "dedak": 9, "lignin": 10.35},
    {"kelas": 2, "sekam": 2, "dedak": 8, "lignin": 10.59},
    {"kelas": 3, "sekam": 3, "dedak": 7, "lignin": 12.31},
    {"kelas": 4, "sekam": 4, "dedak": 6, "lignin": 12.81},
    {"kelas": 5, "sekam": 5, "dedak": 5, "lignin": 13.44},
    {"kelas": 6, "sekam": 6, "dedak": 4, "lignin": 13.50},
    {"kelas": 7, "sekam": 7, "dedak": 3, "lignin": 14.31},
    {"kelas": 8, "sekam": 8, "dedak": 2, "lignin": 16.00},
    {"kelas": 9, "sekam": 9, "dedak": 1, "lignin": 16.07},
    {"kelas": 10, "sekam": 10, "dedak": 0, "lignin": 16.16},
]

# Fungsi untuk memproses gambar
def process_image(file):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Memproses gambar
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (64, 64)).flatten()
    img = img.reshape(1, -1)  # Ubah bentuk untuk prediksi

    return img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        img = process_image(file)

        # Prediksi kelas
        predicted_class = model.predict(img)[0]

        # Ambil data dari tabel berdasarkan kelas yang diprediksi
        result = next((item for item in data_tabel if item["kelas"] == predicted_class), None)

        return render_template('index.html', result=result)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
