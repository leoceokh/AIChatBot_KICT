import os
import logging
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import random
import openai

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# YouTube API setup
DEVELOPER_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# OpenAI API setup
openai.api_key = os.getenv('OPENAI_API_KEY')

if not DEVELOPER_KEY:
    raise ValueError("YouTube API key not set. Please set YOUTUBE_API_KEY in your .env file.")

if not openai.api_key:
    raise ValueError("OpenAI API key not set. Please set OPENAI_API_KEY in your .env file.")

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# Oh Eun-young's channel ID
CHANNEL_ID = 'UCaZS_XwAu1yBMNoQDD1mR7g'

def get_video_info(query):
    try:
        search_response = youtube.search().list(
            channelId=CHANNEL_ID,
            q=query,
            type='video',
            part='id,snippet',
            maxResults=3
        ).execute()

        videos = [
            {
                'title': search_result['snippet']['title'],
                'description': search_result['snippet']['description'],
                'video_id': search_result['id']['videoId']
            }
            for search_result in search_response.get('items', [])
        ]

        if not videos:
            logger.warning(f"No videos found for query: {query}")
        
        return videos
    except HttpError as e:
        logger.error(f'An HTTP error {e.resp.status} occurred:\n{e.content}')
        return None
    except Exception as e:
        logger.error(f'An unexpected error occurred: {str(e)}')
        return None

def generate_counseling_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 오은영 박사입니다. 사용자의 고민에 대해 오은영 박사의 말투와 스타일로 상담해주세요. 답변은 간결하게 해주세요."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        logger.error(f"Error in OpenAI API call: {str(e)}")
        return "죄송합니다. 현재 서비스에 문제가 있습니다. 잠시 후 다시 시도해 주세요."

def generate_chat_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 오은영 박사의 AI 어시스턴트입니다. 사용자와 친절하고 공감적으로 대화해주세요."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        logger.error(f"Error in OpenAI API call: {str(e)}")
        return "죄송합니다. 현재 서비스에 문제가 있습니다. 잠시 후 다시 시도해 주세요."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    print("Chat 요청 받음")  # 로깅 추가
    user_input = request.json['message']
    is_counseling = request.json['isCounseling']
    logger.info(f"Received user input: {user_input}, isCounseling: {is_counseling}")
    
    if is_counseling:
        response = generate_counseling_response(user_input)
        videos = get_video_info(user_input)
    else:
        response = generate_chat_response(user_input)
        videos = None
    
    logger.info(f"Generated response: {response}")
    print("응답 전송")  # 로깅 추가
    return jsonify({'response': response, 'videos': videos})

if __name__ == '__main__':
    app.run(debug=True)