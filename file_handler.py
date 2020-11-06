import time
import logging

from config import Config
from models import models


class FileHandler:
    @staticmethod
    def get_synthesized_audio(text, model_type, **options):
        try:
            results = FileHandler.get_models_results(text, model_type, **options)

            return 0, results

        except Exception as e:
            logging.exception(e)
            return 1, str(e)

    @staticmethod
    def get_models_results(text, model_type, **options):
        if model_type == Config.ALL_MODELS_KEY:
            current_models = {key: val for key, val in models.items() if val is not None}
        else:
            current_models = {model_type: models[model_type]}

        results = []
        for model_name, model in current_models.items():
            start = time.time()
            audio = model.synthesize(text, **options)
            filename = model.save(audio, Config.WAVES_FOLDER)

            with open(filename, "rb") as f:
                audio_bytes = f.read()
            end = time.time()

            results.append(
                {
                    'name': model_name,
                    'time': round(end - start, 3),
                    'filename': filename,
                    'response_audio': audio_bytes
                }
            )

        return results