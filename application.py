import os
import base64
import io
from PIL import Image
import numpy as np
import mlflow.pyfunc
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# MLflow setup
MLFLOW_TRACKING_URI = "https://dagshub.com/sableen-kaur788/KideyDeepLearning.mlflow"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
os.environ["MLFLOW_TRACKING_USERNAME"] = "sableen-kaur788"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "5ce77ae337656ba2215bbed82c8bae34b6ec81f3"

MODEL_NAME = "KidneyTumorModel"

# Load Production model from MLflow
model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/Production")
print(f"✅ Successfully loaded model '{MODEL_NAME}' in Production")

# Flask setup
app = Flask(__name__)
CORS(app)

# Helper: decode base64 → Keras array
def decode_image_to_array(img_str, target_size=(224, 224)):
    img_bytes = base64.b64decode(img_str)
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0  # normalize
    img_array = np.expand_dims(img_array, axis=0)  # (1,H,W,3)
    return img_array

# Routes
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict_route():
    try:
        # Get base64 image
        image_b64 = request.json.get("image")
        if not image_b64:
            return jsonify({"error": "No image provided"}), 400

        # Convert to array
        img_array = decode_image_to_array(image_b64)

        # Directly predict with Keras flavor
        prediction = model.predict(img_array)

        # Convert to label
        pred_label = "Tumor" if prediction[0][0] > 0.5 else "Normal"

        return jsonify([{"image": pred_label}])

    except Exception as e:
        print("❌ Prediction error:", e)
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
