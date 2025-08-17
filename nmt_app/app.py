from flask import Flask, request, jsonify, render_template
from model import translate_text

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def translate():
    languages = {
        'eng_Latn': 'English',
        'hin_Deva': 'Hindi',
        'mar_Deva': 'Marathi',
        'tam_Taml': 'Tamil',
        'ben_Beng': 'Bengali',
    }
    if request.method == 'GET':
        return render_template('home.html', languages=languages,
                                src='eng_Latn', tgt='hin_Deva')
    elif request.method == 'POST':
        text = request.form.get('input_text', None).strip()
        src = request.form.get('source_language_select', 'eng_Latn').strip()
        tgt = request.form.get('target_language_select', 'hin_Deva').strip()
        if text:
            translated = translate_text([text], src, tgt)
            print(text, src, tgt)
            return render_template('home.html', input=text, translated=translated[0],
                               languages=languages, src=src, tgt=tgt)
        else:
            return render_template('home.html', languages=languages,
                                src='eng_Latn', tgt='hin_Deva')
    

if __name__ == '__main__':
    app.run(debug=True)
