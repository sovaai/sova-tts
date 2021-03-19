from tts.synthesizer import Synthesizer, set_logger


ALL_MODELS = "all"

config = Synthesizer.load_config("config.yaml")
set_logger(**config["general"].pop("logging"))

natasha = Synthesizer.from_config(config, name="natasha")

ruslan_config = config["ruslan"]
ruslan = Synthesizer(
    name="ruslan",
    text_handler=natasha.text_handler,
    engine=Synthesizer.module_from_config(ruslan_config, "engine", "tacotron2", natasha.device),
    vocoder=Synthesizer.module_from_config(ruslan_config, "vocoder", "waveglow", natasha.device),
    sample_rate=natasha.sample_rate,
    device=natasha.device,
    pause_type=natasha.pause_type,
    voice_control_cfg=ruslan_config["voice_control_cfg"],
    user_dict=ruslan_config["user_dict"]
)


models = {
    "Natasha": natasha,
    "Ruslan": ruslan,
    ALL_MODELS: None
}