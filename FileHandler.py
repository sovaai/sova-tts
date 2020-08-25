import os
import subprocess
import time
import logging
import uuid
from config import Config
from models import models


class FileHandler:
    @staticmethod
    def getSynthesizedAudio(text, modelType, **options):
        try:
            results = FileHandler.getModelsResults(text, modelType, **options)

            return 0, results

        except Exception as e:
            logging.exception(e)
            return 1, str(e)

    @staticmethod
    def getModelsResults(text, modelType, **options):
        if modelType == Config.ALL_MODELS_KEY:
            currentModels = {key: val for key, val in models.items() if val is not None}
        else:
            currentModels = {modelType: models[modelType]}

        results = []
        for modelName, model in currentModels.items():
            start = time.time()
            audio, filename = model.synthesize(text, **options)
            audioBytes = None
            with open(filename, "rb") as f:
                audioBytes = f.read()
            end = time.time()
            results.append(
                {
                    'name': modelName,
                    'time': round(end - start, 3),
                    'filename': filename,
                    'response_audio': audioBytes
                }
            )

        return results

