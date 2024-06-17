# train_model.py
import numpy as np
import joblib
import os
import cv2
from sklearn.naive_bayes import GaussianNB

# Path ke dataset gambar dedak
dataset_path = '../images/'

# Membaca dataset gambar dedak
def load_dataset(path):
    X = []
    y = []
    for root, dirs, files in os.walk(path):
        for file in files:
            img_path = os.path.join(root, file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (64, 64))
            img_flat = img.flatten()
            X.append(img_flat)
            label = int(file.split('_')[1].split('.')[0])  # Ambil kelas dari nama file
            y.append(label)
    return np.array(X), np.array(y)

# Load dataset
X_train, y_train = load_dataset(dataset_path)

# Train the model
model = GaussianNB()
model.fit(X_train, y_train)

# Simpan model
joblib.dump(model, 'model/pnn_model.pkl')

print("Model telah disimpan di model/pnn_model.pkl")
