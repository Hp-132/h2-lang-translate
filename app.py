
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

def translate(text, source_lang, target_lang):
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f"{source_lang}|{target_lang}"
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("responseData", {}).get("translatedText", "Translation failed")
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route('/')
def home():
    return render_template('lang1.html')  

@app.route('/translate', methods=['GET'])
def translate_api():
    text = request.args.get('text')
    source_lang = request.args.get('source_lang')
    target_lang = request.args.get('target_lang')

    if not text or not source_lang or not target_lang:
        return jsonify({"error": "Missing text, source, or target language"}), 400

    translated_text = translate(text, source_lang, target_lang)
    return jsonify({"translated_text": translated_text})

if __name__ == '__main__':
    app.run(debug=True)
