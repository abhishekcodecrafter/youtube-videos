from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route('/video-info', methods=['GET'])
def get_video_info():
    # Get the video URL from query parameters
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # Initialize YouTube object with the video URL
        yt = YouTube(video_url)

        # Gather video details
        title = yt.title
        thumbnail_url = yt.thumbnail_url

        # Gather stream information
        streams = [
            {
                'resolution': stream.resolution,
                'url': stream.url
            }
            for stream in yt.streams.filter(progressive=True)
        ]

        return jsonify({
            'title': title,
            'thumbnail_url': thumbnail_url,
            'streams': streams
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
