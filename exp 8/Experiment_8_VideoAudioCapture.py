"""
Experiment 8: Capture video/audio from webcam or microphone.
Displays webcam feed and records audio input.
"""

import cv2
import sounddevice as sd
from scipy.io.wavfile import write

def capture_video():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Webcam Capture', frame)
        if cv2.waitKey(1) == 27:  # ESC key
            break
    cap.release()
    cv2.destroyAllWindows()

def record_audio(duration=5, filename="audio_record.wav"):
    print("Recording audio...")
    fs = 44100
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    write(filename, fs, recording)
    print("Audio saved as", filename)

if __name__ == "__main__":
    record_audio()
    capture_video()
