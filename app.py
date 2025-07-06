from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import os
import logging
from tensorflow.keras.models import load_model
import cv2
import tensorflow as tf
from PIL import Image
import io
import traceback
import json
import requests
from datetime import datetime

HUGGINGFACE_API_URL = "https://router.huggingface.co/nebius/v1/chat/completions"
HUGGINGFACE_API_KEY = "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"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configure GPU for TensorFlow (optional)
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    try:
        for device in physical_devices:
            tf.config.experimental.set_memory_growth(device, True)
        logger.info("GPU memory growth enabled")
    except Exception as e:
        logger.error(f"Memory growth config failed: {e}")

# Load the pneumonia detection model
model_path = 'model/model.h5'
if not os.path.exists(model_path):
    raise FileNotFoundError("Model not found at model/model.h5")

try:
    model = load_model(model_path)
except Exception as e:
    logger.error(f"Model loading error: {e}")
    raise

img_width, img_height = 150, 150
threshold = 0.5
recent_predictions = {}

def process_image_with_pil(file_data):
    try:
        img = Image.open(io.BytesIO(file_data)).convert('RGB')  # Load as RGB
        img = img.resize((img_width, img_height))
        img_array = np.array(img) / 255.0  # Shape: (150, 150, 3)
        return img_array, img.size
    except Exception as e:
        logger.error(f"Image processing failed: {e}")
        return None, None

@app.route('/')
def index():
    return jsonify({"status": "Backend is running"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files.get('file')
        if not file or file.filename == '':
            return jsonify({"error": "No file uploaded"}), 400

        file_data = file.read()
        img_array, _ = process_image_with_pil(file_data)
        if img_array is None:
            return jsonify({"error": "Unsupported image format"}), 400

        img_array = np.expand_dims(img_array, axis=0)  # Shape: (1, 150, 150, 3)
        prediction = model.predict(img_array)
        probability = float(prediction[0][0])

        result = {
            "result": "Pneumonia" if probability > threshold else "Normal",
            "probability": probability,
            "confidence": f"{(probability * 100):.2f}%" if probability > threshold else f"{((1 - probability) * 100):.2f}%",
            "interpretation": "High likelihood of pneumonia detected" if probability > threshold else "No signs of pneumonia detected",
            "recommendation": "Consult a healthcare professional" if probability > threshold else "No immediate concern",
            "note": "This is an AI-assisted analysis. Consult a doctor for a professional diagnosis."
        }

        prediction_id = datetime.now().strftime("%Y%m%d%H%M%S")
        recent_predictions[prediction_id] = {
            "filename": file.filename,
            "result": result["result"],
            "probability": probability,
            "timestamp": datetime.now().isoformat()
        }

        return jsonify(result)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({"error": "Image processing failed", "details": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        # Get the most recent prediction if available
        recent_pred = next(reversed(recent_predictions.values()), None) if recent_predictions else None
        
        # Updated: Keep prompt user-facing and warm only
        system_prompt = """You are PneumoScan AI, a helpful and empathetic medical assistant specializing in pneumonia detection.
Respond like a friendly healthcare provider: explain things simply, avoid internal reasoning or planning steps in your answers. 
Focus only on answering the user's questions in a warm, conversational tone. Never reveal internal logic or thought process.
Always remind the user to consult a real doctor for medical advice."""

        context = ""
        if recent_pred:
            confidence = float(recent_pred['probability'])
            diagnosis = "likely positive for pneumonia" if confidence > 0.5 else "likely negative for pneumonia"
            context = f"""
User's most recent chest X-ray analysis:
- Diagnosis: {diagnosis} (confidence: {confidence:.0%})
- File: {recent_pred['filename']}
- Time: {recent_pred['timestamp']}
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{context if context else 'No recent scan results available.'}\n\nUser question: {user_message}"}
        ]

        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": messages,
            "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 300,
                "return_full_text": False,
                "repetition_penalty": 1.2
            },
            "model": "deepseek-ai/DeepSeek-V3-0324-fast"
        }

        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        reply = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        if not reply:
            raise ValueError("No response content found in API response")

        return jsonify({
            "choices": [{
                "message": {
                    "content": reply
                }
            }],
            "usage": result.get("usage", {}),
            "context_used": bool(context)
        })

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return jsonify({
            "error": f"I'm having trouble connecting to the AI service. Please try again later. Error: {str(e)}"
        }), 503
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "error": f"An unexpected error occurred. Please try again. Error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
