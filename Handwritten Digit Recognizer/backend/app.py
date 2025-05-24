from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf

app = Flask(__name__)
CORS(app)

model = tf.keras.models.load_model("mnist_cnn.h5")

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files['image']
    img = Image.open(file).convert("L")  # Convert to grayscale
    img = ImageOps.invert(img)           # Invert: black digit on white bg
    img = img.resize((28, 28))           # Resize to 28x28

    # Normalize and reshape
    img_arr = np.array(img).astype("float32") / 255.0
    img_arr = img_arr.reshape(1, 28, 28, 1)

    # Predict
    prediction = model.predict(img_arr)
    predicted_digit = int(np.argmax(prediction))

    return jsonify({"digit": predicted_digit})
if __name__ == "__main__":
    app.run(debug=True)
