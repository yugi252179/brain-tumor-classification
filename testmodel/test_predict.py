import tensorflow as tf
import cv2
import numpy as np

# Load the model
model = tf.keras.models.load_model('brain_tumor_model.keras')

# Define the labels
labels = ['glioma_tumor', 'no_tumor', 'meningioma_tumor', 'pituitary_tumor']

def preprocess_image(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (150, 150))
    return img.reshape(1, 150, 150, 3)

# Load the image
img=cv2.imread('image(90).jpg')
  # Replace with your image name img = 



if img is None:
    print("Image not found. Check the file path.")
    exit()

processed_img = preprocess_image(img)

# Predict
prediction = model.predict(processed_img)
predicted_class = np.argmax(prediction)
print("Predicted Class:", labels[predicted_class])
print("Prediction Confidence:", 100 * np.max(prediction), "%")
