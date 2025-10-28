"""
Experiment 9: Application to send/receive multimedia messages (text, image, audio).
This is a local demo using Tkinter for UI.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

messages = []

def send_message():
    msg = text_input.get("1.0", tk.END).strip()
    if msg:
        messages.append(("Text", msg))
        chat_box.insert(tk.END, f"You: {msg}\n")
        text_input.delete("1.0", tk.END)

def send_file(file_type):
    file_path = filedialog.askopenfilename()
    if file_path:
        messages.append((file_type, file_path))
        chat_box.insert(tk.END, f"Sent {file_type}: {file_path}\n")

root = tk.Tk()
root.title("Multimedia Messenger")

chat_box = scrolledtext.ScrolledText(root, width=60, height=20)
chat_box.pack(pady=10)

text_input = tk.Text(root, height=3, width=50)
text_input.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Send Text", command=send_message).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Send Image", command=lambda: send_file("Image")).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Send Audio", command=lambda: send_file("Audio")).grid(row=0, column=2, padx=5)

root.mainloop()
