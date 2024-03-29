import json
from flask import Flask, request, jsonify
import youtube_dl
from ytmusicapi import YTMusic
from pytube import YouTube
import os



app = Flask(__name__)
yt = YTMusic(auth=json.loads(os.environ.get('OAUTH_JSON_CONTENT', '{}')))

@app.route('/search', methods=['GET'])
def search_song():
    keyword = request.args.get('keyword')
    results = yt.search(keyword, filter='songs', limit=5)
    response = [{'id': result['videoId'], 'title': result['title'], 'artist': result['artists'][0]['name']} for result in results]
    return jsonify(response)

@app.route('/getstream', methods=['GET'])
def get_stream():
    song_id = request.args.get('songid')
    song_url = f"https://music.youtube.com/watch?v={song_id}"
    try:
        url = ''
        ydl_opts = {
            'youtube_skip_dash_manifest': True,
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'extractaudio': True,
            'audioformat': 'mp3',
            'preferredcodec': 'mp3',
            'nocheckcertificate': True,
            'format_limit': 1,
            'max_downloads': 1,
                    }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song_url, download=False)
            url = info['formats'][0]['url']
        return jsonify({'stream_url': url})
    except:
        yt = YouTube(f'https://www.youtube.com/watch?v={song_id}')
        url = yt.streams.filter(only_audio=True).first().url
        return jsonify({'stream_url': url})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
