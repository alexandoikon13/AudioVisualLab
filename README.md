# AudioVisualLab: Web-Based Audio Processing Application  [AudioVisualLab Web-app](https://audio-visual-lab-aa6ac17b6bff.herokuapp.com/upload)

## Project Overview
This project presents a web-based application designed for audio processing. It offers users the ability to upload audio files, apply various audio processing techniques, and download the processed output. The application is built with a focus on ease of use, allowing users to effortlessly transform their audio files through an intuitive web interface.

## Key Features
- Audio File Upload: Users can upload audio files directly to the cloud for processing.
- Processing Options: Includes functionalities like crossfading between two audio tracks, smoothing audio edges, and converting audio formats.
- Cloud-Based Storage: Utilizes Cloudcube, an AWS S3-based add-on, for robust and scalable storage of audio files.
- Download Processed Files: Users can download the processed audio files through generated links.

## Technologies and Tools Used
- Flask: A lightweight WSGI web application framework in Python, used to create the web server and handle HTTP requests.
- MongoDB: A NoSQL database used for storing metadata about the audio files and processing details.
- Cloudcube: An AWS S3-based storage solution integrated into the app for storing audio files, both original and processed.
- Librosa and Soundfile: Python libraries used for audio processing tasks like format conversion, crossfade, and smoothing edges.
- Docker: Used for containerizing the application, ensuring consistency across various development and deployment environments.
- Heroku: A cloud platform used to deploy and host the web application, offering seamless integration with GitHub for continuous deployment.

## Containerization and Deployment
The application is containerized using Docker, which encapsulates the application and its dependencies in a container. This approach ensures that the application runs consistently across different environments, solving the "it works on my machine" problem. The Docker container includes the Flask app, necessary Python libraries, and configuration to communicate with MongoDB and Cloudcube.
Deployment is handled via Heroku, a popular cloud platform. Heroku integrates seamlessly with Docker, allowing for straightforward deployment of containerized applications. The use of Heroku simplifies the process of scaling, managing, and troubleshooting the app, making it widely accessible to users with minimal setup.

## How It Works
- Upload: Users upload an audio file, which is then stored in Cloudcube.
- Process: Users select an audio processing action and, if necessary, configure additional parameters.
- Storage and Metadata: The processed file is stored back in Cloudcube, and metadata about the processing is saved in MongoDB.
- Download: Users receive a link to download the processed audio file.

## Future Scope (ToDOs)
- Expanded Audio Processing Features: Plans to include more complex audio processing capabilities.
- User Interface Enhancements: Continuous improvements for a more interactive and user-friendly experience.
- Performance Optimization: Ongoing efforts to enhance the efficiency and speed of audio processing.
