"""
Experiment 7: Multimedia Application integrating image, sound, and video.
This simple app uses Tkinter for UI, OpenCV for video, and Pygame for sound.
"""

import cv2
import pygame
import threading
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk

# Initialize pygame mixer for sound
pygame.mixer.init()

def play_sound():
    pygame.mixer.music.load("example.mp3")  # Replace with a valid .mp3 file path
    pygame.mixer.music.play()

def start_video():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) == 27:  # ESC key
            break
    cap.release()
    cv2.destroyAllWindows()

def show_image():
    img = Image.open("example.jpg")  # Replace with a valid image file path
    img.show()

root = tk.Tk()
root.title("Multimedia Application")

Label(root, text="Simple Multimedia App", font=("Arial", 16)).pack(pady=10)

Button(root, text="Show Image", command=show_image).pack(pady=5)
Button(root, text="Play Sound", command=play_sound).pack(pady=5)
Button(root, text="Start Video", command=lambda: threading.Thread(target=start_video).start()).pack(pady=5)

root.mainloop()
