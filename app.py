from flask import Flask, render_template, request, redirect
import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
import os

# Define template and static directory paths
template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Load the trained model
model = tf.keras.models.load_model('brain_tumor_model.keras', compile=False)
model.compile(optimizer=keras.optimizers.RMSprop(), loss='categorical_crossentropy', metrics=['accuracy'])

# Define class labels
labels = ['glioma_tumor', 'no_tumor', 'meningioma_tumor', 'pituitary_tumor']

def preprocess_image(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (150, 150))
    img = img.reshape(1, 150, 150, 3)
    return img

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_label = None
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '':
            return redirect(request.url)

        file = request.files['file']
        if file:
            img_array = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if img is not None:
                processed_img = preprocess_image(img)
                prediction = model.predict(processed_img)
                predicted_class = np.argmax(prediction)
                prediction_label = labels[predicted_class]

    return render_template('index.html', prediction=prediction_label)

if __name__ == '__main__':
    app.run(debug=True)
