from flask import Flask, request, jsonify
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "LegalEase AI Backend is Running!", "status": "ok"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '') if data else ''
    groq_key = os.getenv('GROQ_API_KEY')
    if groq_key:
        try:
            from groq import Groq
            client = Groq(api_key=groq_key)
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are LegalEase AI, a legal assistant for Indian law."},
                    {"role": "user", "content": user_message}
                ]
            )
            answer = completion.choices[0].message.content
            return jsonify({"reply": answer})
        except Exception as e:
            return jsonify({"reply": f"Error: {str(e)}"})
    else:
        return jsonify({"reply": f"Mock: You asked '{user_message}'. Add GROQ_API_KEY in Render to enable AI."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
