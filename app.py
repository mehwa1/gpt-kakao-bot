from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/webhook", methods=["POST"])
def webhook():
    user_msg = request.json['userRequest']['utterance']

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": """
너는 식자재 상담을 전문으로 하는 친절한 챗봇이야.
아래 정보를 기반으로만 대답해야 해. 그 외 주제는 "죄송해요, 그에 대해서는 안내드릴 수 없습니다."라고 말해.

[식자재 정보]
- 막창: 냉동 1kg당 15,000원, 생물 15,500원, 연육 32,000원.
- 대창: 1kg당 17,000원.
- 천엽: 1근당 13,000원.
- 우설: 1kg당 21,000원.
- 소 부산물: 곱창, 대창, 천엽, 우설 등이 해당됨.
"""
        },
        {"role": "user", "content": user_msg}
    ]
)
    answer = response.choices[0].message.content.strip()

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": answer}}]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
