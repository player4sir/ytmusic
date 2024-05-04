import json
from flask import Flask, request, jsonify
from ytmusicapi import YTMusic
import os



app = Flask(__name__)
yt = YTMusic(auth=json.loads(os.environ.get('OAUTH_JSON_CONTENT', '{}')))

@app.route('/search', methods=['GET'])
def search_song():
    keyword = request.args.get('keyword')
    results = yt.search(keyword, filter='songs,playlists,', limit=30)
    response = [{'id': result['videoId'], 'title': result['title'], 'artist': result['artists'][0]['name']} for result in results]
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
