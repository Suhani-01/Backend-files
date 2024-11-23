from flask import Flask, request, jsonify
import pickle
from feature_extraction1 import extract_features_from_url  # Feature extraction function

app = Flask(__name__)

# Enable CORS to allow browser extension communication
from flask_cors import CORS
CORS(app)

# Load the trained model
with open("phishing_model.pkl", "rb") as file:
    phishing_model = pickle.load(file)

@app.route('/check-url', methods=['POST'])
def check_url():
    try:
        data = request.json
        url = data.get('url')
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Extract features and make a prediction
        features = extract_features_from_url(url)
        prediction = phishing_model.predict([features])[0]
        status = "Safe" if prediction == 1 else "Phishing"
        return jsonify({"url": url, "status": status})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)