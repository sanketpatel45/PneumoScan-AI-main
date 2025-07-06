# PneumoScan-AI

PneumoScan-AI is an AI-driven web application designed to detect pneumonia from chest X-ray images. It utilizes a Convolutional Neural Network (CNN) model for image classification and provides a user-friendly interface through a Flask web application.

## Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Model Architecture](#model-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Overview

Pneumonia is a serious respiratory infection that can be life-threatening if not diagnosed and treated promptly. PneumoScan-AI leverages deep learning techniques to automate the detection of pneumonia from chest X-ray images, assisting healthcare professionals in early diagnosis and treatment planning.

## Dataset

The model is trained on the [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) dataset from Kaggle.
This dataset contains over 5,800 X-ray images categorized into two classes: 'PNEUMONIA' and 'NORMAL'.
The images are organized into respective directories for training and testing purposes.

## Model Architecture

The core of PneumoScan-AI is a Convolutional Neural Network (CNN) that classifies chest X-ray images into 'PNEUMONIA' or 'NORMAL' categories.
The model is trained using Keras with TensorFlow as the backend.
It employs convolutional layers for feature extraction, pooling layers for dimensionality reduction, and fully connected layers for classification.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/dhruvpatel848/PneumoScan-AI.git
   cd PneumoScan-AI
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare the dataset:**

   Download the dataset from [Kaggle](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) and place it in the project directory, maintaining the folder structure as provided.

2. **Train the model:**

   Run the `CNN.ipynb` notebook to train the model on the dataset. Ensure that the dataset path in the notebook matches your local setup.

3. **Run the web application:**

   ```bash
   python app.py
   ```

   The application will start on `http://127.0.0.1:5000/`. Open this URL in your web browser to access the application.

4. **Use the application:**

   Upload a chest X-ray image through the web interface. The application will display the prediction result, indicating whether the image shows signs of pneumonia.

## Project Structure

```
PneumoScan-AI/
├── CNN.ipynb                  # Jupyter notebook for model training
├── app.py                     # Flask application
├── pnuemonia_detection_app.py # Additional application script
├── requirements.txt           # Python dependencies
├── templates/                 # HTML templates for the web app
├── uploads/                   # Directory to store uploaded images
└── .ipynb_checkpoints/        # Jupyter notebook checkpoints
```

## Acknowledgments

- Dataset: [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
- Keras and TensorFlow for model development
- Flask for web application development

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
