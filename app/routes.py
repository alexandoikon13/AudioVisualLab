from flask import render_template, request, send_from_directory, jsonify, redirect, url_for
from werkzeug.utils import secure_filename  # Import secure_filename
from scripts.audio_processing import convert_audio
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
                processed_file_path = convert_audio(filepath)

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
