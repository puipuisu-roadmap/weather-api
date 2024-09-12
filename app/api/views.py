import os
import requests
import redis
import json


from flask import request
from . import api
from .. import limiter

@api.route('/weather', methods=['POST'])
@limiter.limit("5 per minute")
def query_weather():
    location = request.json.get('location')
    date1 = request.json.get('date1')
    date2 = request.json.get('date2')
    
    redis_client = redis.Redis(host=os.environ.get("REDIS_HOST"), 
                               port=os.environ.get("REDIS_PORT"))

    if redis_client.exists(location):
        print('Getting data from Redis')
        return json.loads(redis_client.get(location))
    
    params = f"{location}"
    if date1:
        params += f"/{date1}"
    if date2:
        params += f"/{date2}"
    
    API_KEY = os.environ.get("API_KEY")
    API_URL = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{params}?key={API_KEY}"

    response = requests.get(API_URL)
    
    try:
        print('Getting data from API')
        redis_client.set(location, json.dumps(response.json()), ex=3600)
        return response.json()
    except:
        return response.content