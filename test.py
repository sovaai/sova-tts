from tts.synthesizer import Synthesizer


def main():
    tacotron = Synthesizer.from_config("config.yaml", name="natasha")

    samples = [
        "Съешь же ещё этих мягких французских булок да выпей чаю.",

        "Широкая электрификация южных губерний даст мощный толчок подъёму сельского хозяйства.",

        "В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!"
    ]

    save_path = "data/waves"
    for i, sample in enumerate(samples):
        audio = tacotron.synthesize(
            text=sample
        )

        tacotron.save(audio, save_path, str(i))


if __name__ == "__main__":
    main()