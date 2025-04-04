from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import numpy as np


# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS

# Load YOLO model
model = YOLO("best.pt")  # Update path

# Define calories for each class
calorie_dict = {
    "Chapati": 190,
    "Chicken Tandoor": 230,
    "Chole": 280,
    "Fish Fry": 250,
    "Gajar Halwa": 360,
    "Gulab Jamun": 430,
    "Jalebi": 400,
    "Jeera Rice": 200,
    "Matar Paneer": 365,
    "Modak": 320,
    "Paneer Masala": 350,
    "Panipuri": 180,
    "Prawn Masala": 210,
    "Pulav": 250,
    "Samosa": 308,
    "Vadapav": 290,
}

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        # Read image
        image_file = request.files['image'].read()
        np_img = np.frombuffer(image_file, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Run YOLO model
        results = model(img)
        predictions = []

        for result in results:
            probs = result.probs
            if probs is not None:
                top_class_index = probs.top1
                predicted_class = result.names.get(top_class_index, "Unknown")
                confidence = probs.data[top_class_index].item()
                calories = calorie_dict.get(predicted_class, "Unknown")

                predictions.append({
                    "food_item": predicted_class,
                    "confidence": round(confidence, 2),
                    "calories": f"{calories} kcal"
                })

        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)


