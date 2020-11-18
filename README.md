# SOVA TTS

SOVA TTS is a speech syntthesis solution based on [Tacotron 2](https://arxiv.org/abs/1712.05884) architecture. It is designed as a REST API service and it can be customized (both code and models) for your needs.

## Installation

The easiest way to deploy the service is via docker-compose, so you have to install Docker and docker-compose first. Here's a brief instruction for Ubuntu:

#### Docker installation

*	Install Docker:
```bash
$ sudo apt-get update
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo apt-key fingerprint 0EBFCD88
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
$ sudo usermod -aG docker $(whoami)
```
In order to run docker commands without sudo you might need to relogin.
*   Install docker-compose:
```
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
```

*   (Optional) If you're planning on using CUDA run these commands:
```
$ curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | \
  sudo apt-key add -
$ distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
$ curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
$ sudo apt-get update
$ sudo apt-get install nvidia-container-runtime
```
Add the following content to the file **/etc/docker/daemon.json**:
```json
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    },
    "default-runtime": "nvidia"
}
```
Restart the service:
```bash
$ sudo systemctl restart docker.service
``` 

#### Build and deploy

*   Clone the repository, download the pretrained models archive and extract the contents into the project folder:
```bash
$ git clone --recursive https://github.com/sovaai/sova-tts.git
$ cd sova-tts/
$ wget http://dataset.sova.ai/SOVA-TTS/Data.tar
$ tar -xvf Data.tar && rm Data.tar
```

*   Build docker image
     *   Build *sova-tts-gpu* image if you're planning on using GPU:
     ```bash
     $ sudo docker-compose build sova-tts-gpu
     ```
     *   Build *sova-tts* image if you're planning on using CPU:
     ```bash
     $ sudo docker-compose build sova-tts
     ```

*	Run the desired service container
     *   GPU:
     ```bash
     $ sudo docker-compose up -d sova-tts-gpu
     ```
     *   CPU:
     ```bash
     $ sudo docker-compose up -d sova-tts
     ```

## Testing

To test the service you can send a POST request:
```bash
$ curl --request POST 'http://localhost:8899/synthesize/' --form 'voice=Natasha' --form 'text="Добрый день!"'
```

## Acknowledgements

Original [Tacotron 2](https://github.com/NVIDIA/tacotron2) implementation by NVIDIA.
