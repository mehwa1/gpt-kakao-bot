from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    user_msg = request.json['userRequest']['utterance']

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 식자재에 대해서만 대답하는 친절한 상담 챗봇이야. 다른 주제엔 답하지 마."},
            {"role": "user", "content": user_msg}
        ]
    )
    answer = response['choices'][0]['message']['content'].strip()

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": answer}}]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)