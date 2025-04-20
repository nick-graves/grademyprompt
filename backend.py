from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os

# Allow importing core.py from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import evaluate_prompt

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    user_prompt = data.get("prompt")
    model = data.get("model", "llama3:8b")

    if not user_prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        full_response, score, feedback = evaluate_prompt(user_prompt, model=model)

        # Fake sub-scores until parsing logic is added
        breakdown = {
            "clarity": score // 5,
            "specificity": score // 5,
            "context": score // 5,
            "task": score // 5,
            "alignment": score - (score // 5) * 4
        }

        return jsonify({
            "score": score,
            "feedback": feedback,
            "breakdown": breakdown,
            "raw": full_response
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
