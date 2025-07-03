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
                    "outputs": [{"simpleText": {"text": "사용자의 입력이 없습니다."}}]
                }
            })

        # GPT 응답 생성
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

    except Exception as e:
        # 디버깅용 에러 메시지
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{"simpleText": {"text": f"에러 발생: {str(e)}"}}]
            }
        })
