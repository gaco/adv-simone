# google_reviews.py
# Google Maps Reviews Integration

import os
from datetime import datetime
from typing import Dict, List, Optional

import requests


class GoogleReviewsService:
    """Service to fetch reviews from Google Places API"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GOOGLE_MAPS_API_KEY")
        self.base_url = "https://maps.googleapis.com/maps/api/place"

    def get_place_details(self, place_id: str) -> Dict:
        """Get place details including reviews from Google Places API"""

        if not self.api_key:
            print(
                "⚠️  Google Maps API key not configured. No Google reviews will be shown."
            )
            return {"reviews": []}

        try:
            # Google Places API endpoint for place details
            url = f"{self.base_url}/details/json"
            params = {
                "place_id": place_id,
                "fields": "name,rating,reviews,user_ratings_total",
                "key": self.api_key,
                "language": "pt-BR",  # Portuguese reviews
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("status") == "OK":
                return data.get("result", {})
            else:
                print(f"❌ Google Places API error: {data.get('status')}")
                return {"reviews": []}

        except requests.RequestException as e:
            print(f"❌ Error fetching Google reviews: {e}")
            return {"reviews": []}

    def get_formatted_reviews(self, place_id: str) -> List[Dict]:
        """Get formatted reviews ready for template display"""

        place_data = self.get_place_details(place_id)
        reviews = place_data.get("reviews", [])

        formatted_reviews = []

        for review in reviews:
            try:
                # Format Google review for our template
                comment = review.get("text", "")
                # Clean empty or quote-only comments
                if (
                    comment
                    and comment.strip()
                    and comment.strip() not in ['""', "''", '"""', "'''"]
                ):
                    clean_comment = comment.strip()
                else:
                    clean_comment = ""

                formatted_review = {
                    "client_name": review.get("author_name", "Cliente Google"),
                    "rating": review.get("rating", 5),
                    "comment": clean_comment,
                    "source": "google",
                    "date_created": self._format_google_date(review.get("time")),
                    "profile_photo": review.get("profile_photo_url", ""),
                    "relative_time": review.get("relative_time_description", ""),
                }
                formatted_reviews.append(formatted_review)
            except Exception as e:
                print(f"⚠️  Error formatting review: {e}")
                continue

        return formatted_reviews

    def _format_google_date(self, timestamp: Optional[int]) -> datetime:
        """Convert Google timestamp to datetime object"""
        if timestamp:
            try:
                return datetime.fromtimestamp(timestamp)
            except (ValueError, TypeError):
                pass
        return datetime.now()


def get_place_id_from_url(google_maps_url: str) -> Optional[str]:
    """Extract Place ID from Google Maps URL - for future implementation"""
    # This would require parsing the URL or using Google's URL API
    # For now, we'll use the manually configured Place ID
    return None


# Convenience function for easy import
def get_google_reviews(place_id: str, api_key: Optional[str] = None) -> List[Dict]:
    """Get Google reviews for a place ID"""
    if not place_id:
        print("⚠️  Google Place ID not configured. No Google reviews will be shown.")
        return []

    service = GoogleReviewsService(api_key)
    return service.get_formatted_reviews(place_id)
