from flask import render_template, request, send_from_directory, jsonify, redirect, send_file, url_for
from werkzeug.utils import secure_filename  # Import secure_filename
from scripts.audio_processing import load_audio, save_audio, crossfade, smooth_edges, convert_audio_format, process_and_save_audio
from datetime import datetime
import gridfs
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

        # Test if the file was uploaded successfully to the Heroku server
        if not os.path.exists(filepath):
            print(f"File not found at {filepath}")
        else:
            print(f"File saved at {filepath}")

        audio, sr = load_audio(filepath)
        processed_audio = None

        if action == 'crossfade':
            processed_audio = crossfade(audio, audio, int(0.5 * sr))  # 0.5 seconds crossfade
        elif action == 'smooth_edges':
            processed_audio = smooth_edges(audio, int(0.1 * sr))  # 0.1 seconds smoothing at edges

        processed_filename = 'processed_' + filename
        processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
        save_audio(processed_audio, sr, processed_filepath)

        # Store the processed file in GridFS
        fs = gridfs.GridFS(app.db)
        with open(processed_filepath, 'rb') as processed_file:
            file_id = fs.put(processed_file, filename=processed_filename)
        
        # Store file metadata in MongoDB
        file_metadata = {
        'original_filename': filename,
        'processed_filename': processed_filename,
        'processing_type': action,
        'processed_datetime': datetime.utcnow(),
        'gridfs_id': file_id
        }
        app.db.files.insert_one(file_metadata)

        return send_from_directory(app.config['UPLOAD_FOLDER'], processed_filename, as_attachment=True)
    
    @app.route('/convert', methods=['POST'])
    def convert():
        file = request.files['file']
        target_format = request.form['format']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        output_path = convert_audio_format(filepath, target_format)
        print("Saved file at:", output_path)  # Log the file path

        return send_file(output_path, as_attachment=True)

    @app.route('/crossfade', methods=['POST'])
    def crossfade_audio():
        file1 = request.files['file1']
        file2 = request.files['file2']
        crossfade_duration = float(request.form.get('crossfade_duration', 1.0))

        filename1 = secure_filename(file1.filename)
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        file1.save(filepath1)

        filename2 = secure_filename(file2.filename)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        file2.save(filepath2)

        audio1, sr = load_audio(filepath1)
        audio2, _ = load_audio(filepath2)
        crossfade_samples = int(sr * crossfade_duration)
        crossfaded_audio = crossfade(audio1, audio2, crossfade_samples)

        output_filename = 'crossfaded_' + filename1
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        save_audio(crossfaded_audio, sr, output_filepath)

        return send_file(output_filepath, as_attachment=True)

    @app.route('/smooth_edges', methods=['POST'])
    def smooth_audio_edges():
        file = request.files['file']
        edge_duration = float(request.form.get('edge_duration', 0.5))

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        audio, sr = load_audio(filepath)
        edge_samples = int(sr * edge_duration)
        smoothed_audio = smooth_edges(audio, edge_samples)

        output_filename = 'smoothed_' + filename
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        save_audio(smoothed_audio, sr, output_filepath)

        return send_file(output_filepath, as_attachment=True)

    @app.route('/some_route', methods=['POST'])
    def some_route():
        file = request.files['file']  # Retrieve the uploaded file
        # Assuming the file content is what needs to be processed and saved
        file_content = file.read()

        # Process and save the file content
        processed_file_path = process_and_save_audio(file_content)

        # Now send this file back
        return send_file(processed_file_path, as_attachment=True)
    