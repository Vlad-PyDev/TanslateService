from flask import Flask, render_template, request, redirect, url_for
from translate import Translator

app = Flask(__name__)

translations_en_to_ru = {
  'hello': 'привет',
  'world': 'мир',
  'goodbye': 'до свидания'
}
translations_ru_to_en = {
  'привет': 'hello',
  'мир': 'world',
  'до свидания': 'goodbye'
}
translation_history = []


def translate_text(text, from_lang='ru', to_lang='en'):
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    try:
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        return f"Error: {e}"


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/main', methods=['GET', 'POST'])
def main():
  result = None
  word = None
  direction = None
  if request.method == 'POST':
    word = request.form.get('word').strip()
    direction = request.form.get('direction')
    try:
      result = translate_text(request.form.get('word').strip(), from_lang=direction.split('-')[0], to_lang=direction.split('-')[1])
    except:
      result = translations_ru_to_en.get(word.lower(), "Translation not found")
    translation_history.append({'word': word, 'direction': direction, 'result': result})
  return render_template('main.html', result=result, word=word, direction=direction, history=translation_history)


if __name__ == '__main__':
  app.run(debug=True)