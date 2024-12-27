# backend/app.py

from flask import Flask, request, jsonify
from services.controller import process_input
from database.feedback_service import FeedbackService
from database.factory import get_repository

app = Flask(__name__)

# Initialize database and feedback service
repository = get_repository()
feedback_service = FeedbackService(repository)


@app.route("/process", methods=["POST"])
def process():
    data = request.json
    user_input = data.get("user_input")
    model = data.get("model")
    zip_code = data.get("zip_code")
    if not user_input or not model or not zip_code:
        return jsonify({"error": "Missing required fields"}), 400
    response = process_input(user_input, model, zip_code)
    return jsonify({"response": response})


@app.route("/feedback", methods=["POST"])
def add_feedback():
    data = request.json
    model = data.get("model")
    user_input = data.get("user_input")
    output = data.get("output")
    feedback_service.add_feedback(model, user_input, output)
    return jsonify({"status": "success"})


@app.route("/feedback", methods=["GET"])
def get_feedback():
    feedback = feedback_service.get_feedback()
    return jsonify(feedback)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
