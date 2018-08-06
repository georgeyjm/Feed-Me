import pyaudio
import wave
import sys
import random
from flask import Flask

app = Flask(__name__)

CHUNK = 4096

wfs = ['chew1.wav', 'chew2.wav']

@app.route('/play')
def play():
    p = pyaudio.PyAudio()
    wf = wave.open(random.choice(wfs), 'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
