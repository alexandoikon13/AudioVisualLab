from flask import render_template, request, send_from_directory, jsonify, redirect, url_for
from werkzeug.utils import secure_filename  # Import secure_filename
from scripts.audio_processing import load_audio, save_audio, crossfade, smooth_edges
import os

def init_routes(app):
    @app.route('/')
    def index():
        return redirect(url_for('upload'))

    @app.route('/upload')
    def upload():
        return render_template('upload.html')

    @app.route('/handle_upload', methods=['POST'])
    def handle_upload():
        file = request.files['file']
        action = request.form.get('action')
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        audio, sr = load_audio(filepath)
        processed_audio = None

        if action == 'crossfade':
            # Example: crossfade with itself for demonstration
            processed_audio = crossfade(audio, audio, int(0.5 * sr))  # 0.5 seconds crossfade
        elif action == 'smooth_edges':
            processed_audio = smooth_edges(audio, int(0.1 * sr))  # 0.1 seconds smoothing at edges

        processed_filename = 'processed_' + filename
        processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
        save_audio(processed_audio, sr, processed_filepath)

        return send_from_directory(app.config['UPLOAD_FOLDER'], processed_filename, as_attachment=True)


########################################################################
#########################  START TODO ##################################       
    @app.route('/convert', methods=['POST'])
    def convert():
        # Handle file upload and call convert_audio_format
        # ...
        return None

    @app.route('/crossfade', methods=['POST'])
    def crossfade_audio():
        # Ensure all lines within this function are indented at the same level
        if 'file1' in request.files and 'file2' in request.files:
            # Further code for handling crossfade
            pass  # Replace with actual code

        # More code or return statement
        return "Crossfade processed"

    @app.route('/smooth_edges', methods=['POST'])
    def smooth_audio_edges():
        # Implement logic for smoothing edges of an audio file
        # ...
        return None

#########################  END TODO ##################################
########################################################################   
