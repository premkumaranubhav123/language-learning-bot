from flask import Flask, render_template, request
from googletrans import Translator
import os

app = Flask(__name__)

# Initialize empty lists to store message history
message_history = []

@app.route('/')
def home():
    return render_template('base.html', message_history=message_history)

@app.route('/translate', methods=['POST'])
def translate():
    if request.method == 'POST':
        input_text = request.form['input_text']
        dest_lang = request.form['dest_lang']

        # If a valid language is selected, perform translation
        if dest_lang != 'Choose Language' and input_text:
            translator = Translator()
            translated = translator.translate(text=input_text, dest=dest_lang)
            translated_text = translated.text
            
            # Append the latest message and translation to the history
            message_history.append({
                'input_text': input_text,
                'dest_lang': dest_lang,
                'translated_text': translated_text
            })

            # Keep only the last 15 messages in history
            if len(message_history) > 15:
                message_history.pop(0)

            return render_template('base.html', translated_text=translated_text, dest_lang=dest_lang, input_text=input_text, message_history=message_history)
        else:
            error_message = "Please select a destination language and enter some text."
            return render_template('base.html', error_message=error_message, message_history=message_history)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT from environment, default to 5000
    app.run(debug=True, host='0.0.0.0', port=port)
