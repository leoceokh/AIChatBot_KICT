from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import traceback

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not client.api_key:
        return jsonify({'error': "OpenAI API 키가 설정되지 않았습니다."}), 500

    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'error': "메시지가 비어 있습니다."}), 400
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = response.choices[0].message.content
        return jsonify({'response': bot_response})
    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f"서버 오류: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
