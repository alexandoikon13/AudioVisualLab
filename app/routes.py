from flask import render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename  # Import secure_filename
from scripts.audio_processing import load_audio, save_audio, crossfade, smooth_edges, convert_audio_format
from scripts.cloudcube_utils import upload_file_to_cloudcube, get_cloudcube_file_url
from datetime import datetime
import os

def init_routes(app):

    @app.route('/')
    def index():
        return redirect(url_for('upload'))


    @app.route('/upload')
    def upload():
        return render_template('upload.html')


    @app.route('/process_file', methods=['POST'])
    def process_file():
        file = request.files['file']
        action = request.form.get('action')
        filename = secure_filename(file.filename)
        file_content = file.read()

        # Upload original file to Cloudcube & Retrieve URL
        upload_file_to_cloudcube(file_content, filename, file.content_type)
        file_url = get_cloudcube_file_url(filename)

        # Initialize processed_filename
        processed_filename = filename  # Default to original filename

        # Process the file based on the action
        audio, sr = load_audio(file_content)
        processed_audio = None

        if action == 'convert':
            target_format = request.form.get('format', 'wav')
            processed_audio, format_used = convert_audio_format(file_content, target_format)
            processed_filename = os.path.splitext(filename)[0] + '.' + format_used
        elif action == 'crossfade':
            crossfade_duration = float(request.form.get('crossfade_duration', 1.0))  # seconds
            processed_audio = crossfade(audio, audio, int(sr * crossfade_duration))
            processed_filename = f"crossfaded_{filename}"
        elif action == 'smooth_edges':
            edge_duration = float(request.form.get('edge_duration', 0.5))
            processed_audio = smooth_edges(audio, int(sr * edge_duration))
            processed_filename = f"smoothed_{filename}"

        # Handle cases where no processing is required
        if processed_audio is not None:
            processed_file_content = save_audio(processed_audio, sr)
            # Upload processed file to Cloudcube & Retrieve URL
            upload_file_to_cloudcube(processed_file_content, processed_filename, f'audio/{target_format if action == "convert" else "wav"}')
            processed_file_url = get_cloudcube_file_url(processed_filename)
        else:
            # If no processing, return original file URL
            processed_file_content = file_content
            processed_file_url = file_url
            return jsonify({"message": "File uploaded successfully! No action was taken!", "url": file_url})       

        # Upload processed file to Cloudcube & Retrieve URL
        upload_file_to_cloudcube(processed_file_content, processed_filename, f'audio')
        processed_file_url = get_cloudcube_file_url(processed_filename)

        # Store file metadata in MongoDB
        file_metadata = {
            'original_filename': filename,
            'processed_filename': processed_filename,
            'processing_type': action,
            'processed_datetime': datetime.utcnow(),
            'original_file_url': file_url,
            'processed_file_url': processed_file_url
        }
        app.db.files.insert_one(file_metadata)

        # return jsonify({"message": "File processed and uploaded successfully", "url": processed_file_url})
        
        # Return an HTML response with a download link
        return render_template('download.html', file_url=processed_file_url)


    @app.route('/convert', methods=['POST'])
    def convert():
        file = request.files['file']
        target_format = request.form['format']
        filename = secure_filename(file.filename)
        file_content = file.read()

        # Upload original file to Cloudcube
        upload_file_to_cloudcube(file_content, filename, file.content_type)
        original_file_url = get_cloudcube_file_url(filename)

        # Convert the file format
        converted_content, format_used = convert_audio_format(file_content, target_format)
        converted_filename = os.path.splitext(filename)[0] + '.' + format_used

        # Upload converted file to Cloudcube
        upload_file_to_cloudcube(converted_content, converted_filename, 'audio')  # Adjust MIME type accordingly
        converted_file_url = get_cloudcube_file_url(converted_filename)

        # Store file metadata in MongoDB
        file_metadata = {
            'original_filename': filename,
            'converted_filename': converted_filename,
            'conversion_format': format_used,
            'converted_datetime': datetime.utcnow(),
            'original_file_url': original_file_url,
            'converted_file_url': converted_file_url
        }
        app.db.files.insert_one(file_metadata)

        return jsonify({"message": "File converted and uploaded successfully", "url": converted_file_url})


    @app.route('/crossfade', methods=['POST'])
    def crossfade_audio():
        file1 = request.files['file1']
        file2 = request.files['file2']
        crossfade_duration = float(request.form.get('crossfade_duration', 1.0))

        filename1 = secure_filename(file1.filename)
        file_content1 = file1.read()
        upload_file_to_cloudcube(file_content1, filename1, file1.content_type)

        filename2 = secure_filename(file2.filename)
        file_content2 = file2.read()
        upload_file_to_cloudcube(file_content2, filename2, file2.content_type)

        audio1, sr1 = load_audio(file_content1)
        audio2, sr2 = load_audio(file_content2)

        crossfade_samples = int(min(sr1, sr2) * crossfade_duration)
        crossfaded_audio = crossfade(audio1, audio2, crossfade_samples)

        crossfaded_filename = 'crossfaded_' + filename1
        crossfaded_content = save_audio(crossfaded_audio, min(sr1, sr2))
        upload_file_to_cloudcube(crossfaded_content, crossfaded_filename, 'audio')

        crossfaded_file_url = get_cloudcube_file_url(crossfaded_filename)

        # Store file metadata in MongoDB
        file_metadata = {
            'file1': filename1,
            'file2': filename2,
            'crossfaded_filename': crossfaded_filename,
            'crossfade_duration': crossfade_duration,
            'crossfaded_datetime': datetime.utcnow(),
            'crossfaded_file_url': crossfaded_file_url
        }
        app.db.files.insert_one(file_metadata)

        return jsonify({"message": "Crossfade processed and uploaded successfully", "url": crossfaded_file_url})


    @app.route('/smooth_edges', methods=['POST'])
    def smooth_audio_edges():
        file = request.files['file']
        edge_duration = float(request.form.get('edge_duration', 0.5))

        filename = secure_filename(file.filename)
        file_content = file.read()
        upload_file_to_cloudcube(file_content, filename, file.content_type)

        audio, sr = load_audio(file_content)
        edge_samples = int(sr * edge_duration)
        smoothed_audio = smooth_edges(audio, edge_samples)

        smoothed_filename = 'smoothed_' + filename
        smoothed_content = save_audio(smoothed_audio, sr)
        upload_file_to_cloudcube(smoothed_content, smoothed_filename, 'audio')

        smoothed_file_url = get_cloudcube_file_url(smoothed_filename)

        # Store file metadata in MongoDB
        file_metadata = {
            'original_filename': filename,
            'smoothed_filename': smoothed_filename,
            'edge_duration': edge_duration,
            'smoothed_datetime': datetime.utcnow(),
            'smoothed_file_url': smoothed_file_url
        }
        app.db.files.insert_one(file_metadata)

        return jsonify({"message": "Edges smoothed and uploaded successfully", "url": smoothed_file_url})
