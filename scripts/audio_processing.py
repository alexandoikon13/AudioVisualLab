import librosa
import soundfile as sf
import numpy as np
import os
import io

# Function to load an audio file from byte content
def load_audio(file_content):
    # Use BytesIO to create a file-like object from the byte content
    with io.BytesIO(file_content) as buffer:
        audio, sr = librosa.load(buffer, sr=None)  # sr=None to keep original sample rate
    return audio, sr

# Function to save an audio file
def save_audio(audio, sample_rate, format='wav'):
    with io.BytesIO() as buffer:
        # Ensure audio data is in the correct shape
        if len(audio.shape) == 1:  # Mono audio
            audio = np.expand_dims(audio, axis=-1)
        # Save audio to a BytesIO object and return its content
        sf.write(buffer, audio, sample_rate, format=format)
        return buffer.getvalue()


# Function to convert an audio file format
def convert_audio_format(file_content, output_format):
    # Load the audio from the file content
    audio, sr = librosa.load(io.BytesIO(file_content), sr=None)

    # Convert and save the audio to the desired format
    with io.BytesIO() as buffer:
        # Handle format-specific details here
        if output_format in ['wav', 'flac', 'mp3']:
            # For formats supported by soundfile
            sf.write(buffer, audio, sr, format=output_format)
        else:
            # For unsupported formats, additional handling is needed
            # You may need to use a different library or provide a fallback
            raise NotImplementedError(f"Format '{output_format}' is not supported.")

        buffer.seek(0)  # Rewind to the beginning of the buffer
        return buffer.read(), output_format

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
