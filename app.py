import requests
from flask import Flask, request, render_template
import os
from dotenv import load_dotenv
load_dotenv()  # Nimmt die Umgebungsvariablen aus der .env-Datei auf

app = Flask(__name__)

api_key = os.environ.get('OPENAI_API_KEY')

def send_chat_request(api_key, content):
    try:
        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
        data = {
            "model": "gpt-4",
            "messages": [
            {"role": "system", "content": "Du bist ein Professor, der in fachsprache Antwortet. Antworte zunächst auf Deutsch. Danach antworte auf Spanisch.  "},
            {"role": "user", "content": content}
        ]
    }

        response = requests.post(api_url, headers=headers, json=data)
        return response.json()
    except Exception as e:
        print(f"Fehler bei der API-Anfrage: {e}")
        return {"choices": [{"message": {"content": "Es gab ein Problem bei der Verbindung mit der API."}}]}

   



@app.route('/', methods=['GET', 'POST'])
def index():
    response = ""
    if request.method == 'POST':
        content = request.form['content']
        chatgpt_response = send_chat_request(api_key, content)
        response = chatgpt_response.get("choices", [{}])[0].get("message", {}).get("content", "")
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)


