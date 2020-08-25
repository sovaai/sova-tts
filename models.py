import sys
from config import Config


models = {
    Config.ALL_MODELS_KEY: None  # run all models
}

# tacotron2
sys.path.insert(0, "modules/tts")
from modules.tts.Tacotron import Tacotron
models["Natasha"] = Tacotron('config.yaml', name="natasha")
models["Ruslan"] = Tacotron('config.yaml', name="ruslan")
