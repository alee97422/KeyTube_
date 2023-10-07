#Author: Anthony Lee 
#this is a program that will simply take the youtube URL via user input and it will then take that url and it 
#download it 
#convert to mp3
#give user the option to delete video to preserve space
#analyze mp3 file and try to determine the KEY that this "song" in 
#I am doing this to help me determine musical KEY so that i can play music along with some of my favorite tunes with my guitar


import ttkbootstrap as ttk
from pytube import YouTube
from moviepy.editor import VideoFileClip
import tkinter.messagebox as msgbox
import os
import pygame
import librosa
import librosa.display
import numpy as np

# Initialize pygame mixer
pygame.mixer.init()

# Initialize global variable for video
video = None

# Function to download the video and convert to MP3
def download_and_convert_video():
    global video  # Declare video as a global variable
    url = url_entry.get()
    
    try:
        # Create a YouTube object
        video = YouTube(url)
    
        # Choose the stream with the desired quality (e.g., '720p')
        video_stream = video.streams.filter(res="720p").first()
    
        # Download the video to the current directory
        video_stream.download()
    
        # Get the filename of the downloaded video
        video_filename = f"{video.title}.mp4"
        
        # Perform the MP4 to MP3 conversion
        video_clip = VideoFileClip(video_filename)
        audio_clip = video_clip.audio
        mp3_filename = f"{video.title}.mp3"
        audio_clip.write_audiofile(mp3_filename)
        audio_clip.close()
        
        # Ask the user if they want to delete the original MP4 file
        user_response = msgbox.askyesno("Delete Original", "Do you want to delete the original MP4 video?")
        
        if user_response:
            # Delete the original MP4 file if the user chooses to
            video_clip.close()
            os.remove(video_filename)
        
        result_label.config(text="Conversion complete!")

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

# Function to play the converted MP3 file
def play_audio():
    mp3_filename = f"{video.title}.mp3"
    pygame.mixer.music.load(mp3_filename)
    pygame.mixer.music.play()

# Function to analyze the key of the audio
def analyze_audio():
    mp3_filename = f"{video.title}.mp3"
    
    try:
        # Load the audio file
        y, sr = librosa.load(mp3_filename)
        
        # Compute the chromagram
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        
        # Estimate the key
        key = np.argmax(np.mean(chroma, axis=1))
        
        # Map key index to musical note
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        key_note = notes[key]
        
        result_label.config(text=f"Success! The key is {key_note}")

    except Exception as e:
        result_label.config(text="Unsuccessful read! Please try a different URL or video of the same content.")

# Create a ttk themed window
root = ttk.Window(themename="vapor")
root.title("Youtube URL and Key")

frame = ttk.Frame(root, padding=10)
frame.grid(column=0, row=0, sticky=(ttk.W, ttk.E, ttk.N, ttk.S))

url_label = ttk.Label(frame, text="YouTube URL:")
url_label.grid(column=0, row=0, sticky=ttk.W)

url_entry = ttk.Entry(frame, width=40)
url_entry.grid(column=0, row=1, columnspan=2, pady=5)

download_button = ttk.Button(frame, text="Download and Convert to MP3", command=download_and_convert_video)
download_button.grid(column=1, row=2)

play_button = ttk.Button(frame, text="Play Audio", command=play_audio)
play_button.grid(column=0, row=2)

analyze_button = ttk.Button(frame, text="Analyze Key", command=analyze_audio)
analyze_button.grid(column=1, row=3)

result_label = ttk.Label(frame, text="")
result_label.grid(column=0, row=4, columnspan=2, pady=10)

# Start the tkinter main loop
root.mainloop()
