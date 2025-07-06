import streamlit as st
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Sequential


# Define paths to your data
train_dir = "C:\\Users\\cathe\\Downloads\\chest_xray\\train"
test_dir = "C:\\Users\\cathe\\Downloads\\chest_xray\\test"
val_dir = "C:\\Users\\cathe\\Downloads\\chest_xray\\val"

# Define image dimensions and batch size
img_width, img_height = 150, 150
batch_size = 32

# Data Augmentation
train_datagen = ImageDataGenerator(rescale=1. / 255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)


train_generator = train_datagen.flow_from_directory(train_dir,
                                                    target_size=(img_width, img_height),
                                                    batch_size=batch_size,
                                                    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(val_dir,
                                                        target_size=(img_width, img_height),
                                                        batch_size=batch_size,
                                                        class_mode='binary')

# Balance the data
normal_images = len(os.listdir(os.path.join(train_dir, 'NORMAL')))
pneumonia_images = len(os.listdir(os.path.join(train_dir, 'PNEUMONIA')))
if normal_images > 0 and pneumonia_images > 0:
    total_samples = normal_images + pneumonia_images
    weight_for_0 = (1 / normal_images) * (total_samples) / 2.0
    weight_for_1 = (1 / pneumonia_images) * (total_samples) / 2.0
    class_weight = {0: weight_for_0, 1: weight_for_1}
else:
    raise ValueError("One or more classes have no images in the training data.")

# Model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 3)),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Flatten(),
    Dense(512, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])



# Streamlit app title
st.title("Pneumonia Detection App")

# File uploader for uploading X-ray images
uploaded_image = st.file_uploader("Upload an X-ray image", type=["jpg", "png", "jpeg"])

# Function to preprocess image
def preprocess_image(image):
    # Convert image to RGB
    img_rgb = image.convert("RGB")
    # Resize image
    resized_image = img_rgb.resize((img_width, img_height))
    # Convert image to numpy array
    img_array = np.array(resized_image)
    # Normalize pixel values
    normalized_image = img_array / 255.0
    # Add batch dimension
    input_image = np.expand_dims(normalized_image, axis=0)
    return input_image

# Function to make predictions
def predict_pneumonia(image):
    input_image = preprocess_image(image)
    pred = model.predict(input_image)
    return pred


# Display uploaded image and make predictions
if uploaded_image is not None:
    # Display uploaded image
    image = Image.open(BytesIO(uploaded_image.read()))
    st.image(image, caption='Uploaded X-ray Image.', use_column_width=True)

    # Make predictions
    if st.button('Detect Pneumonia'):
        pred = predict_pneumonia(image)
        st.write("Predictions and Probabilities:")
        if pred[0][0] >= 0.5:
            st.write("Pneumonia Detected")
        else:
            st.write("No Pneumonia Detected")
