from flask import Flask, request
import os

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No video part", 400

    video = request.files['video']
    if video.filename == '':
        return "No selected file", 400

    # Save the video file
    video_path = os.path.join("uploads", video.filename)
    video.save(video_path)

    # Here, you would process the video using your AI model
    # For example: process_video(video_path)

    return "Video processed", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Change port if needed
