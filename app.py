import json
from flask import Flask, request, jsonify
from ytmusicapi import YTMusic
import os

app = Flask(__name__)
yt = YTMusic(auth=json.loads(os.environ.get('OAUTH_JSON_CONTENT', '{}')),language='zh_CN',location='US')

@app.route('/search', methods=['GET'])
def search_song():
    keyword = request.args.get('keyword')
    results = yt.search(keyword, filter='songs', limit=30)
    response = []
    for result in results:
        if 'artists' in result and len(result['artists']) > 0:
            response.append({
                'id': result.get('videoId', ''),
                'title': result.get('title', ''),
                'artist': result['artists'][0].get('name', '')
            })
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
