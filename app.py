from base64 import b64encode

from flask import Flask, render_template, request, send_from_directory, url_for
from flask_cors import CORS, cross_origin

from models import models
from config import Config
from file_handler import FileHandler


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

_valid_model_types = [key for key in models if key is not Config.ALL_MODELS_KEY]


@app.route('/', methods=["GET"])
@cross_origin()
def index():
    return render_template("speechSynthesis.html", existing_models=models.keys())


def parse_options(options):
    options = options.replace(" ", "")
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


@app.route("/get_models/", methods=["POST"])
@cross_origin()
def get_models():
    response_code = 1
    try:
        result = _valid_model_types
        response_code = 0
    except Exception as e:
        result = str(e)

    return {
        "response_code": response_code,
        "response": result
    }


@app.route("/synthesize/", methods=["POST"])
@cross_origin()
def synthesize():
    text = request.form["text"]
    options = request.form.get("options")
    model_type = request.form.get("voice")

    try:
        options = parse_options(options)
    except:
        options = {}

    response_code, results = FileHandler.get_synthesized_audio(text, model_type, **options)

    if response_code == 0:
        for result in results:
            filename = result.get("filename", None)
            audio_bytes = result.get("response_audio", None)
            result["response_audio_url"] = url_for("media_file", filename=filename)
            result["response_audio"] = b64encode(audio_bytes).decode("utf-8")

    return {
        "response_code": response_code,
        "response": results
    }


class InvalidVoice(Exception):
    pass

@app.route("/get_user_dict/", methods=["POST"])
@cross_origin()
def get_user_dict():
    request_json = request.get_json()

    model_type = request_json.get("voice")

    response_code = 1
    try:
        if model_type not in _valid_model_types:
            raise InvalidVoice("Parameter 'voice' must be one of the following: {}".format(_valid_model_types))

        model = models[model_type]
        result = model.get_user_dict()

        response_code = 0
    except InvalidVoice as e:
        result = str(e)
    except Exception as e:
        result = str(e)

    return {
        "response_code": response_code,
        "response": result
    }


@app.route("/update_user_dict/", methods=["POST"])
@cross_origin()
def update_user_dict():
    request_json = request.get_json()

    model_type = request_json.get("voice")
    user_dict = request_json.get("user_dict")

    response_code = 1
    try:
        if model_type not in _valid_model_types:
            raise InvalidVoice("Parameter 'voice' must be one of the following: {}".format(_valid_model_types))

        model = models[model_type]
        model.update_user_dict(user_dict)

        result = "User dictionary has been updated"
        response_code = 0
    except InvalidVoice as e:
        result = str(e)
    except Exception as e:
        result = str(e)

    return {
        "response_code": response_code,
        "response": result
    }


@app.route("/replace_user_dict/", methods=["POST"])
@cross_origin()
def replace_user_dict():
    request_json = request.get_json()

    model_type = request_json.get("voice")
    user_dict = request_json.get("user_dict")

    response_code = 1
    try:
        if model_type not in _valid_model_types:
            raise InvalidVoice("Parameter 'voice' must be one of the following: {}".format(_valid_model_types))

        model = models[model_type]
        model.replace_user_dict(user_dict)

        result = "User dictionary has been replaced"
        response_code = 0
    except InvalidVoice as e:
        result = str(e)
    except Exception as e:
        result = str(e)

    return {
        "response_code": response_code,
        "response": result
    }


@app.route("/media/<path:filename>", methods=["GET"])
@cross_origin()
def media_file(filename):
    return send_from_directory(Config.MEDIA, filename, as_attachment=False)