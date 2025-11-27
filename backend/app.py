from flask import Flask, request, jsonify
from ai.response_engine import ask_gemini

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"health_check": True}), 200

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data["question"]
    context = data["context"]
    answer = ask_gemini(question, context)
    return jsonify({
      "answer": answer
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
