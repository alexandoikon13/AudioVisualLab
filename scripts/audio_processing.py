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

def convert_audio_format(input_path, output_path):
    data, samplerate = sf.read(input_path)
    sf.write(output_path, data, samplerate)

# Crossfade function
def crossfade(audio1, audio2, crossfade_samples):
    fade_out = np.linspace(1, 0, crossfade_samples)
    fade_in = np.linspace(0, 1, crossfade_samples)

    overlap1 = audio1[-crossfade_samples:] * fade_out
    overlap2 = audio2[:crossfade_samples] * fade_in

    return np.concatenate((audio1[:-crossfade_samples], overlap1 + overlap2, audio2[crossfade_samples:]))

def logarithmic_crossfade(audio1, audio2, crossfade_samples):
    fade_out = np.logspace(0, -1, crossfade_samples)
    fade_in = np.logspace(-1, 0, crossfade_samples)

    overlap1 = audio1[-crossfade_samples:] * fade_out
    overlap2 = audio2[:crossfade_samples] * fade_in

    return np.concatenate((audio1[:-crossfade_samples], overlap1 + overlap2, audio2[crossfade_samples:]))

# Smooth edges function
def smooth_edges(audio, edge_samples):
    if edge_samples > 0:
        fade_in = np.linspace(0, 1, edge_samples)
        fade_out = np.linspace(1, 0, edge_samples)

        audio[:edge_samples] *= fade_in
        audio[-edge_samples:] *= fade_out
    
    return audio

# Load the entire song
audio, sr = load_audio('WhatsApp_Audio.mp3')

# Specify the start and end time in seconds of the part to be removed
start_time = 21.03
end_time = 21.32

# Convert time to samples
start_sample = librosa.time_to_samples(start_time, sr=sr)
end_sample = librosa.time_to_samples(end_time, sr=sr)

# Cut the part out
part1 = audio[:start_sample]
part2 = audio[end_sample:]

# Define crossfade duration in seconds (adjust as needed)
crossfade_duration = (end_time - start_time)*0.943975  # crossfade_duration = 0.5
crossfade_samples = librosa.time_to_samples(crossfade_duration, sr=sr)
part1_normalized = librosa.util.normalize(part1)
part2_normalized = librosa.util.normalize(part2)

# Apply crossfade
# audio_crossfaded = crossfade(part1, part2, crossfade_samples)
# audio_crossfaded = crossfade(part1_normalized, part2_normalized, crossfade_samples)
audio_crossfaded = logarithmic_crossfade(part1_normalized, part2_normalized, crossfade_samples)

# Apply smoothing to the cut edges (adjust duration as needed)
edge_smoothing_duration = (end_time - start_time)*0.15   # edge_smoothing_duration = 0.5  # seconds
edge_samples = librosa.time_to_samples(edge_smoothing_duration, sr=sr)
audio_smoothed = smooth_edges(audio_crossfaded, edge_samples)

# Normalize the audio
normalized_audio = librosa.util.normalize(audio_smoothed)

# Save the final audio
save_audio(normalized_audio, sr, 'final_song_normalized.wav')  # saving as WAV
