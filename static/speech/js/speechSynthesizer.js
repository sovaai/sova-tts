String.prototype.format = function () {
    a = this;
    for (k in arguments) {
        a = a.replace("{" + k + "}", arguments[k])
    }
    return a
};

function send_form() {
    // If the user has pressed enter on textarea
    if (window.event.keyCode === 13) {
        TEXT_FIELD = document.getElementById("text-input");
        VOICE = document.getElementById("model-select-id")
        PITCH_FACTOR = document.getElementById("pitch");
        SPEED_FACTOR = document.getElementById("rate");
        VOLUME_FACTOR = document.getElementById("volume");
        ERROR_FIELD = document.getElementById("error_field");
        SYNTHESIS_RESULT = document.getElementById("table_body_result");

        TEXT_FIELD.readOnly = true;
        ERROR_FIELD.style.display = "none";

        var data = {
            "text": TEXT_FIELD.value,
            "voice": VOICE.value,
            "rate": SPEED_FACTOR.value,
            "pitch": PITCH_FACTOR.value,
            "volume": VOLUME_FACTOR.value
        }

        fetch("/synthesize/", {
                method: "post",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
             })
            .then((response) => {
                if (!response.ok) throw response;
                return response.json();
            })
            .then((response) => {
                SYNTHESIS_RESULT.innerHTML = "";
                response_code = response["response_code"];
                results = response["response"];

                if (response_code === 0) {
                    results.forEach(function (model_ans) {
                        SYNTHESIS_RESULT.insertAdjacentHTML(
                            "beforeend",
                            TR_PATTERN.format(
                                model_ans["response_audio_url"],
                                model_ans["synthesis_time"],
                                model_ans["voice"]
                            )
                        );
                    });
                } else {
                    ERROR_FIELD.innerHTML = "Error: " + response;
                    ERROR_FIELD.style.display = "block";
                }
                TEXT_FIELD.readOnly = false;
            })
            .catch((err) => {
                console.log(err);
                err.text().then((errorMessage) => {
                    ERROR_FIELD.innerHTML = errorMessage;
                    ERROR_FIELD.style.display = "block";
                    TEXT_FIELD.readOnly = false;
                });
            });

    };
};

var TR_PATTERN = `
    <tr>
        <td>
            <audio controls preload="none">
                <source src="{0}" type="audio/wav">
                Your browser does not support audio.
            </audio>
        </td>
        <td>{1}</td>
        <td>{2}</td>
    </tr>
`;
