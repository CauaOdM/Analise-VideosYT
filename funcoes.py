from dotenv import load_dotenv
import re
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import google.generativeai as genai

load_dotenv(".env.local")

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY not found in environment variables (.env or .env.local).")

genai.configure(api_key=api_key)

def extrair_ID_video(url):
    video_id = url.split("v=")[1]
    return video_id

def transcript_video(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
    formatter = TextFormatter()
    text_formatted = formatter.format_transcript(transcript)
    return text_formatted

