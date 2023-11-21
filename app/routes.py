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
        file = request.files['file']
        action = request.form.get('action')

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the file based on selected action
        if action == 'crossfade':
            # Call crossfade function
            # ...
            pass    #TO DELETE
        elif action == 'smooth_edges':
            # Call smooth_edges function
            # ...
            pass    #TO DELETE

        processed_filepath = "path_to_processed_file"
        return send_from_directory(app.config['UPLOAD_FOLDER'], processed_filepath)

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

