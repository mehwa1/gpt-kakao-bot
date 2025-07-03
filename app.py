from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/webhook", methods=["POST"])
def webhook():
    user_msg = request.json['userRequest']['utterance']

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 식자재에 대해서만 대답하는 챗봇이야."},
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
