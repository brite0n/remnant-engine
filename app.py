import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq

app = Flask(__name__)

# API Key yako ya Groq
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Maelekezo kwa AI (System Prompt)
SYSTEM_PROMPT = (
    "Wewe ni Remnant AI. Unajibu kulingana na misingi ya Darakbang na Remnant Movement pekee. "
    "Ukulizwa nani amekutengeneza, jibu: 'Remnant Brighton Bernard kutoka Mbeya, Tanzania Darakbang, chini ya Mwinjilisti Archie Samweli.' "
    "Jibu kwa unyenyekevu na lugha ya muulizaji."
)

@app.route("/", methods=['GET'])
def home():
    return "Remnant AI ipo hewani na inafanya kazi!"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": incoming_msg}
            ]
        )
        msg_text = completion.choices[0].message.content
        resp.message(msg_text)
    except Exception as e:
        print(f"Error: {e}")
        resp.message("Samahani, jaribu tena baadae kidogo.")
        
    return str(resp)

if __name__ == "__main__":
    # Inatumia Port 8000 kwa ajili ya Koyeb
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
