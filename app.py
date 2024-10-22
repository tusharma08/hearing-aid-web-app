from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import numpy as np
import pyaudio
from threading import Thread
from audio_processing import process_audio_data  # Import the audio processing logic

app = Flask(__name__)
socketio = SocketIO(app)

SAMPLE_RATE = 44100  # Sample rate in Hz
CHUNK = 1024         # Number of frames per buffer

# Global variable for PyAudio stream
stream_in = None
stream_out = None
p = None

def initialize_pyaudio():
    global p, stream_in, stream_out

    p = pyaudio.PyAudio()

    # Open audio stream for input (microphone)
    stream_in = p.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=SAMPLE_RATE,
                       input=True,
                       frames_per_buffer=CHUNK)

    # Open audio stream for output (speakers)
    stream_out = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=SAMPLE_RATE,
                        output=True,
                        frames_per_buffer=CHUNK)

def cleanup():
    global p, stream_in, stream_out
    if stream_in is not None:
        stream_in.stop_stream()
        stream_in.close()
    if stream_out is not None:
        stream_out.stop_stream()
        stream_out.close()
    if p is not None:
        p.terminate()

@socketio.on('start_audio')
def start_audio(data):
    amplification_factor = data['amplificationFactor']
    noise_reduction_level = data['noiseReductionLevel']

    def stream_audio():
        try:
            initialize_pyaudio()

            while True:
                # Read audio data from the microphone
                audio_data = stream_in.read(CHUNK)
                
                # Convert audio data to numpy array
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                
                # Amplify and process the audio signal with noise reduction
                processed_data = process_audio_data(audio_array, amplification_factor, noise_reduction_level)

                # Emit processed audio data to the frontend
                socketio.emit('audio_data', {'data': processed_data.tolist()})

                # Output the processed audio to the speaker
                stream_out.write(processed_data.tobytes())

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            cleanup()

    # Start the audio processing in a new thread
    Thread(target=stream_audio).start()

@socketio.on('stop_audio')
def stop_audio():
    cleanup()

@app.route('/')
def index():
    return render_template('index.html')

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
