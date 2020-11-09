from config import Config
from modules.tts.synthesizer import Synthesizer


config = Synthesizer.load_config("data/config.yaml")

natasha = Synthesizer.from_config(config, name="natasha")
ruslan = Synthesizer.from_config(config, name="ruslan")

models = {
    "Natasha": natasha,
    "Ruslan": ruslan,
    Config.ALL_MODELS_KEY: None
}