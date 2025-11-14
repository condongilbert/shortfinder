import os
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class YouTubeAPI:
    """Wrapper for YouTube Data API to search and retrieve Shorts."""

    def __init__(self, api_key: str):
        """Initialize YouTube API client.

        Args:
            api_key: YouTube Data API key
        """
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.shorts_duration = 60  # YouTube Shorts are <= 60 seconds

    def search_shorts(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search for YouTube Shorts by query.

        Args:
            query: Search query string
            max_results: Maximum number of results to return

        Returns:
            List of video data with metadata
        """
        try:
            request = self.youtube.search().list(
                q=query,
                part="snippet",
                maxResults=max_results,
                videoDuration="short",  # Videos <= 4 minutes
                videoType="video",
                order="relevance",
                type="video",
            )
            response = request.execute()

            shorts = []
            for item in response.get("items", []):
                video_id = item["id"].get("videoId")
                if video_id:
                    short_data = {
                        "video_id": video_id,
                        "title": item["snippet"].get("title"),
                        "description": item["snippet"].get("description"),
                        "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                        "channel_title": item["snippet"].get("channelTitle"),
                        "published_at": item["snippet"].get("publishedAt"),
                    }
                    shorts.append(short_data)

            return shorts

        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            raise

    def get_video_details(self, video_id: str) -> Optional[Dict]:
        """Get detailed information about a specific video.

        Args:
            video_id: YouTube video ID

        Returns:
            Dictionary with video details or None if not found
        """
        try:
            request = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=video_id,
            )
            response = request.execute()

            if response.get("items"):
                item = response["items"][0]
                duration = item["contentDetails"].get("duration", "")

                video_details = {
                    "video_id": video_id,
                    "title": item["snippet"].get("title"),
                    "description": item["snippet"].get("description"),
                    "channel_id": item["snippet"].get("channelId"),
                    "channel_title": item["snippet"].get("channelTitle"),
                    "published_at": item["snippet"].get("publishedAt"),
                    "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                    "duration": duration,
                    "view_count": item["statistics"].get("viewCount", 0),
                    "like_count": item["statistics"].get("likeCount", 0),
                    "comment_count": item["statistics"].get("commentCount", 0),
                    "tags": item["snippet"].get("tags", []),
                    "category_id": item["snippet"].get("categoryId"),
                }

                return video_details
            else:
                return None

        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            raise

    def get_trending_shorts(
        self, region_code: str = "US", max_results: int = 10
    ) -> List[Dict]:
        """Get trending YouTube Shorts for a specific region.

        Args:
            region_code: ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB')
            max_results: Maximum number of results to return

        Returns:
            List of trending video data
        """
        try:
            request = self.youtube.videos().list(
                part="snippet,statistics",
                maxResults=max_results,
                regionCode=region_code,
                videoDuration="short",
                order="viewCount",
                chart="mostPopular",
            )
            response = request.execute()

            trending = []
            for item in response.get("items", []):
                trending_data = {
                    "video_id": item["id"],
                    "title": item["snippet"].get("title"),
                    "description": item["snippet"].get("description"),
                    "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                    "channel_title": item["snippet"].get("channelTitle"),
                    "published_at": item["snippet"].get("publishedAt"),
                    "view_count": item["statistics"].get("viewCount", 0),
                }
                trending.append(trending_data)

            return trending

        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            raise

    def get_channel_shorts(self, channel_id: str, max_results: int = 10) -> List[Dict]:
        """Get YouTube Shorts from a specific channel.

        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of results to return

        Returns:
            List of channel shorts data
        """
        try:
            request = self.youtube.search().list(
                part="snippet",
                channelId=channel_id,
                maxResults=max_results,
                videoDuration="short",
                videoType="video",
                order="date",
                type="video",
            )
            response = request.execute()

            shorts = []
            for item in response.get("items", []):
                video_id = item["id"].get("videoId")
                if video_id:
                    short_data = {
                        "video_id": video_id,
                        "title": item["snippet"].get("title"),
                        "description": item["snippet"].get("description"),
                        "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                        "published_at": item["snippet"].get("publishedAt"),
                    }
                    shorts.append(short_data)

            return shorts

        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            raise
