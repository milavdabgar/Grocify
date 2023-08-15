from flask import Blueprint, render_template
from app.routes.cart_routes import get_cart_count
import os
import requests

bp = Blueprint('recipe_routes', __name__)

@bp.route('/recipe')
def recipe():
    # checks items on the cart
    cart_count = get_cart_count()
    return render_template('recipes_dbmeal.html', cart_count=cart_count)


@bp.route('/videos')
def videos():
    # Configure your YouTube API key and channel ID
    api_key = os.environ.get('YT_API_KEY')

    # Define the search query for cooking videos
    search_query = 'Indian Cooking Recipes'

    # Make a request to the YouTube API
    url = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&part=snippet&type=video&q={search_query}'
    response = requests.get(url)
    data = response.json()

    # Extract the video information from the API response
    videos = []
    for item in data['items']:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        video_thumbnail = item['snippet']['thumbnails']['medium']['url']
        videos.append({'id': video_id, 'title': video_title, 'thumbnail': video_thumbnail})

    # Limit the number of videos to a maximum of 10
    videos = videos[:10]

    cart_count = get_cart_count()
    
    # Render the template and pass the videos to it
    return render_template('recipes_youtube.html', videos=videos, cart_count=cart_count)