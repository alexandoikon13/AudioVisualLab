from flask import render_template, request, send_from_directory, send_file, jsonify, redirect, url_for
from werkzeug.utils import secure_filename  # Import secure_filename
from scripts.audio_processing import load_audio, save_audio, crossfade, logarithmic_crossfade, smooth_edges
import os

def init_routes(app):

    @app.route('/')
    def index():
        # return 'Welcome to the File Converter App'
        return redirect(url_for('upload'))

    @app.route('/upload')
    def upload():
        return render_template('upload.html')

    @app.route('/handle_upload', methods=['POST'])  # Changed to a different endpoint
    def handle_upload():
        try:
            if 'file' not in request.files:
                return "No file part", 400
            file = request.files['file']
            if file.filename == '':
                return "No selected file", 400
            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Process the file
                processed_file_path = convert_audio_format(filepath)

                # Save file metadata to MongoDB
                file_metadata = {
                    "original_filename": filename,
                    "processed_filepath": processed_file_path
                }
                app.db.files.insert_one(file_metadata)

                return "File uploaded and processed", 200
        except Exception as e:
            app.logger.error('Failed to upload file', exc_info=e)
            return "Internal Server Error", 500
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
    @app.route('/convert', methods=['POST'])
    def convert():
        file = request.files['file']
        target_format = request.form['format']
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)
        
        output_path = os.path.splitext(input_path)[0] + '.' + target_format
        convert_audio_format(input_path, output_path)
        
        return send_file(output_path, as_attachment=True)

