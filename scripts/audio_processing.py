import librosa
import soundfile as sf
import numpy as np

# Function to load an audio file
def load_audio(file_path):
    audio, sr = librosa.load(file_path, sr=None)  # sr=None to keep original sample rate
    return audio, sr

# Function to save an audio file
def save_audio(audio, sample_rate, file_path):
    sf.write(file_path, audio, sample_rate)

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

# Add other processing functions as needed
