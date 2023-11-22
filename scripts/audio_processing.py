import librosa
import soundfile as sf
import numpy as np
import os
import io

# Function to load an audio file from byte content
def load_audio(file_content):
    # Use BytesIO to create a file-like object from the byte content
    with io.BytesIO(file_content) as file_like_object:
        audio, sr = librosa.load(file_like_object, sr=None)  # sr=None to keep original sample rate
    return audio, sr

# Function to save an audio file
def save_audio(audio, sample_rate):
    # Save audio to a BytesIO object and return its content
    with io.BytesIO() as buffer:
        sf.write(buffer, audio, sample_rate, format='wav')
        return buffer.getvalue()

# Funtion to apply Crossfade between two audio segments
def crossfade(audio1, audio2, crossfade_samples):
    fade_out = np.linspace(1, 0, crossfade_samples)
    fade_in = np.linspace(0, 1, crossfade_samples)
    overlap1 = audio1[-crossfade_samples:] * fade_out
    overlap2 = audio2[:crossfade_samples] * fade_in
    return np.concatenate((audio1[:-crossfade_samples], overlap1 + overlap2, audio2[crossfade_samples:]))

# Function to Smooth the edges of an audio segment
def smooth_edges(audio, edge_samples):
    if edge_samples > 0:
        fade_in = np.linspace(0, 1, edge_samples)
        fade_out = np.linspace(1, 0, edge_samples)
        audio[:edge_samples] *= fade_in
        audio[-edge_samples:] *= fade_out
    return audio

# Function to convert an audio file format
def convert_audio_format(file_content, output_format):
    # First, read the audio data from the file content
    audio, sr = librosa.load(io.BytesIO(file_content), sr=None)

    # Then, use a buffer to save the audio in the desired format
    with io.BytesIO() as buffer:
        sf.write(buffer, audio, sr, format=output_format)   # Adjust this part to handle different formats correctly
        buffer.seek(0)  # Rewind to the beginning of the buffer
        return buffer.read()
