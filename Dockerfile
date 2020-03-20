FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y \
    alsa-utils \
    libasound-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    python3-pyaudio 
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD "python ./start.py"
