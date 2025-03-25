from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
import cv2

app = Flask(__name__)
CORS(app)

# Load the trained model
model = tf.keras.models.load_model("rice_disease_model.h5")

# Disease information with suggestions and pesticides
disease_info = {
    "Bacterial Leaf Blight": {
        "suggestion": "Use copper-based bactericides. Avoid overhead irrigation.",
        "pesticide": "Streptomycin or Copper Oxychloride"
    },
    "Blast": {
        "suggestion": "Use resistant varieties. Apply balanced nitrogen fertilizer.",
        "pesticide": "Tricyclazole or Isoprothiolane"
    },
    "Brown Spot": {
        "suggestion": "Improve soil fertility with potassium. Use certified disease-free seeds.",
        "pesticide": "Mancozeb or Propiconazole"
    },
    "Healthy": {
        "suggestion": "Your crop is healthy! Maintain proper irrigation and nutrient balance.",
        "pesticide": "No pesticides needed"
    }
}

# Define route for prediction
@app.route("/predict", methods=["POST"])
def predict():
    print("Received prediction request...")

    if "file" not in request.files:
        print("Error: No file part in request.")
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        print("Error: No selected file.")
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read and process the image
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        
        # Check if the image was loaded correctly
        if image is None:
            print("Error: Unable to decode image.")
            return jsonify({"error": "Unable to decode image"}), 400

        # Convert to grayscale and resize to (28, 28)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (28, 28))
        
        # Normalize the image and reshape it for the model
        image = image / 255.0
        image = np.expand_dims(image, axis=-1)  # Add channel dimension for grayscale
        image = np.expand_dims(image, axis=0)   # Add batch dimension

        # Make prediction
        prediction = model.predict(image)
        predicted_class = np.argmax(prediction)
        
        # Handle the class index and map it to disease
        disease_names = list(disease_info.keys())
        
        if predicted_class >= len(disease_names):
            print("Error: Invalid class prediction.")
            return jsonify({"error": "Invalid prediction"}), 500

        disease_name = disease_names[predicted_class]
        suggestion = disease_info[disease_name]["suggestion"]
        pesticide = disease_info[disease_name]["pesticide"]

        # Return prediction result
        return jsonify({
            "disease": disease_name,
            "suggestion": suggestion,
            "pesticide": pesticide
        })

    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"error": "Error processing image"}), 500


# Run the Flask app
if __name__ == "__main__":
    print("Flask app running on port 5000...")
    app.run(debug=True, host="0.0.0.0", port=5000)
