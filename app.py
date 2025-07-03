from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        body = request.get_json()
        user_msg = body.get('userRequest', {}).get('utterance', '')

        if not user_msg:
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [{"simpleText": {"text": "막창은 냉동 1kg당 1만 5천원, 생물 1만 5천 5백원, 연육 3만 2천원 입니다."}}]
                }
            })

        # GPT 응답 생성
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 친절한 식자재 상담 챗봇이야. 주제가 식자재와 관련이 없으면 대답을 하지 말고 '식자재에 대해서만 답변드릴 수 있어요'라고 말해줘."},
                {"role": "user", "content": user_msg}
            ]
        )
        answer = response['choices'][0]['message']['content'].strip()

        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{"simpleText": {"text": "막창은 냉동 1kg당 1만 5천원, 생물 1만 5천 5백원, 연육 3만 2천원 입니다."}}]
            }
        })

    except Exception as e:
        # 디버깅용 에러 메시지
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{"simpleText": {"text": f"에러 발생: {str(e)}"}}]
            }
        })
