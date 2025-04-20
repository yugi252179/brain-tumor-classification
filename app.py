from flask import Blueprint, render_template, request, redirect, url_for, flash
import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
import os
from werkzeug.utils import secure_filename
import shutil

predict_bp = Blueprint('predict', __name__, template_folder='templates', static_folder='static')

# Upload folder setup
UPLOAD_FOLDER = os.path.join(predict_bp.static_folder, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

predict_bp.config = {}
predict_bp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
predict_bp.secret_key = 'your_predict_secret_key'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'jpg'}



# Load the model
model = None
try:
    model = tf.keras.models.load_model('brain_tumor_model.keras', compile=False)
    model.compile(optimizer=keras.optimizers.RMSprop(), loss='categorical_crossentropy', metrics=['accuracy'])
    print("Brain tumor model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

# Class labels
labels = ['glioma_tumor', 'no_tumor', 'meningioma_tumor', 'pituitary_tumor']



def preprocess_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (150, 150))
    img = img.reshape(1, 150, 150, 3)
    return img
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@predict_bp.route('/', methods=['GET', 'POST'])
def index():
    prediction_label = None
    img_url = None

    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '':
            flash("No file selected.", category='error')
            return redirect(request.url)

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(predict_bp.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            img_url = url_for('.static', filename=f'uploads/{filename}')

            img = cv2.imread(filepath)
            
            if img is not None:
                processed_img = preprocess_image(img)
                prediction = model.predict(processed_img)
                predicted_class = np.argmax(prediction)
                prediction_label = labels[predicted_class]
            else:
                flash("Error reading the uploaded image.", category='error')
        else:
            flash("Invalid file type. Please upload a .jpg image.", category='error')

    return render_template('predict_index.html', prediction=prediction_label, img_url=img_url)

@predict_bp.route('/reset_uploads')
def reset_uploads():
    try:
        shutil.rmtree(predict_bp.config['UPLOAD_FOLDER'])
        os.makedirs(predict_bp.config['UPLOAD_FOLDER'], exist_ok=True)
        flash("Uploads folder has been reset.", category='info')
    except Exception as e:
        flash(f"Error resetting uploads: {e}", category='error')
    return redirect(url_for('.index'))
