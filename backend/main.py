import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from youtube_api import YouTubeAPI

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize YouTube API
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube_api = YouTubeAPI(YOUTUBE_API_KEY)


@app.route("/", methods=["GET"])
def home():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Shortfinder API is running"})


@app.route("/api/shorts/search", methods=["GET"])
def search_shorts():
    """Search for YouTube Shorts by query."""
    try:
        query = request.args.get("q")
        max_results = request.args.get("max_results", default=10, type=int)

        if not query:
            return jsonify({"error": "Query parameter 'q' is required"}), 400

        results = youtube_api.search_shorts(query, max_results)
        return jsonify({"success": True, "data": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/shorts/<video_id>", methods=["GET"])
def get_short_details(video_id):
    """Get details for a specific YouTube Short."""
    try:
        details = youtube_api.get_video_details(video_id)
        if details:
            return jsonify({"success": True, "data": details})
        else:
            return jsonify({"error": "Video not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/shorts/trending", methods=["GET"])
def get_trending_shorts():
    """Get trending YouTube Shorts."""
    try:
        region_code = request.args.get("region", default="US")
        max_results = request.args.get("max_results", default=10, type=int)

        results = youtube_api.get_trending_shorts(region_code, max_results)
        return jsonify({"success": True, "data": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
