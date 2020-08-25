from flask import Flask, render_template, request, send_from_directory, url_for
from config import Config
from FileHandler import FileHandler
from models import models
from base64 import b64encode


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('speechSynthesis.html', existing_models=models.keys())


def parse_options(options):
    options = [opt.strip().split("=") for opt in options.split(",")]

    valid_options = {}
    for opt, value in options:
        if opt == "tone_factor":
            factor = float(value)
            if factor > 1.5 or factor < 0.75:
                continue
            valid_options[opt] = factor
        elif opt == "speed_factor":
            factor = float(value)
            if factor > 2 or factor < 0.5:
                continue
            valid_options[opt] = factor

    return valid_options


@app.route('/tts/', methods=['POST'])
def tts():
    text = request.form['text']
    options = request.form.get('options')
    modelType = request.form.get('voice')

    try:
        options = parse_options(options)
    except:
        options = {}

    responseCode, results = FileHandler.getSynthesizedAudio(text, modelType, **options)

    if responseCode == 0:
        for result in results:
            filename = result.get("filename", None)
            audioBytes = result.get("response_audio", None)
            result["response_audio_url"] = url_for('media_file', filename=filename)
            result["response_audio"] = b64encode(audioBytes).decode("utf-8")

    return {
        'response_code': responseCode,
        'response': results
    }


@app.route('/media/<path:filename>', methods=['GET'])
def media_file(filename):
    return send_from_directory(Config.MEDIA, filename, as_attachment=False)

