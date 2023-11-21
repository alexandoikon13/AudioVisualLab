from pydub import AudioSegment

def convert_audio(input_path, output_format="mp3"):
    audio = AudioSegment.from_file(input_path)
    output_path = input_path.split('.')[0] + '.' + output_format
    audio.export(output_path, format=output_format)
    return output_path

# Use this function in your upload_file route after saving the file
