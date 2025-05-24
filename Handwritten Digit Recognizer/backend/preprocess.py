import numpy as np
from PIL import Image
import io

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('L')
    image = image.resize((28, 28))
    img_array = np.array(image)
    img_array = img_array.reshape(1, 28, 28, 1) / 255.0
    return img_array
