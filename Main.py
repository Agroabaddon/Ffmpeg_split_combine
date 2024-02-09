import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import os

def extract_audio():
    input_file = filedialog.askopenfilename()
    if not input_file:
        return  # User canceled selection
    output_file = "output_audio.aac"
    try:
        process = subprocess.Popen(["ffmpeg", "-i", input_file, "-vn", "-acodec", "copy", output_file], stderr=subprocess.PIPE)
        while process.poll() is None:
            output = process.stderr.readline().decode()
            if output.startswith("frame="):
                progress.set(int(output.split()[2]))
                root.update_idletasks()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showinfo("Success", "Audio extraction complete")

def extract_frames():
    input_file = filedialog.askopenfilename()
    if not input_file:
        return  # User canceled selection
    output_directory = filedialog.askdirectory()
    try:
        process = subprocess.Popen(["ffmpeg", "-i", input_file, "-vf", "fps=1", f"{output_directory}/frame_%04d.png"], stderr=subprocess.PIPE)
        while process.poll() is None:
            output = process.stderr.readline().decode()
            if output.startswith("frame="):
                progress.set(int(output.split()[2]))
                root.update_idletasks()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showinfo("Success", "Frame extraction complete")

def combine_video():
    frames_dir = filedialog.askdirectory()
    if not frames_dir:
        return  # User canceled selection
    audio_file = filedialog.askopenfilename()
    if not audio_file:
        return  # User canceled selection
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if not output_file:
        return  # User canceled selection

    try:
        process = subprocess.Popen(["ffmpeg", "-framerate", "1", "-i", f"{frames_dir}/frame_%04d.png", "-i", audio_file, "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental", output_file], stderr=subprocess.PIPE)
        while process.poll() is None:
            output = process.stderr.readline().decode()
            if output.startswith("frame="):
                progress.set(int(output.split()[2]))
                root.update_idletasks()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showinfo("Success", "Video combination complete")

# Create GUI
root = tk.Tk()
root.title("Video Extraction Tool")

progress = tk.IntVar()
progress_bar = tk.Progressbar(root, orient="horizontal", length=200, mode="determinate", variable=progress)
progress_bar.pack(pady=10)

audio_button = tk.Button(root, text="Extract Audio", command=extract_audio)
audio_button.pack(pady=5)

frames_button = tk.Button(root, text="Extract Frames", command=extract_frames)
frames_button.pack(pady=5)

combine_button = tk.Button(root, text="Combine Video", command=combine_video)
combine_button.pack(pady=5)

root.mainloop()
