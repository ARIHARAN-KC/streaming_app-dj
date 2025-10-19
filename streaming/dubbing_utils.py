import os
import subprocess
import requests
import json
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip
from googletrans import Translator  # Import Google Translate
from pathlib import Path

# Define the storage path for dubbed videos inside your project
BASE_DIR = Path(__file__).resolve().parent  # Current folder of this script
DUBBED_VIDEO_DIR = BASE_DIR / "media" / "dub_videos"

# Ensure the directory exists
os.makedirs(DUBBED_VIDEO_DIR, exist_ok=True)

# Transcribe audio using Whisper
def transcribe_audio(audio_path):
    """
    Transcribe audio to text using OpenAI Whisper.
    """
    try:
        import whisper
        model = whisper.load_model("base")  # Use a small model for free usage
        result = model.transcribe(audio_path)
        return result["text"]
    except ImportError:
        raise Exception("Whisper is not installed. Install it using `pip install openai-whisper`.")

# Translate text using Google Translate (googletrans)
def translate_text(text, target_language):
    """
    Translate text to the target language using Google Translate.
    """
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")

# Convert text to speech using gTTS
def text_to_speech(text, language, output_audio_path):
    """
    Convert text to speech using gTTS.
    """
    from gtts import gTTS
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_audio_path)

# Extract audio from video
def extract_audio_from_video(video_path, output_audio_path):
    """
    Extract audio from a video file.
    """
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_audio_path)

# Merge dubbed audio with video
def merge_audio_with_video(video_path, audio_path, output_video_path):
    """
    Merge the dubbed audio with the original video.
    """
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile(output_video_path, codec="libx264")

# Main dubbing function
def dub_video_with_translation(video_path, target_language):
    """
    Dub a video by translating its audio to the target language.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(DUBBED_VIDEO_DIR, exist_ok=True)

        # Step 1: Extract audio from the video
        audio_path = os.path.join(DUBBED_VIDEO_DIR, os.path.basename(video_path).replace(".mp4", "_original_audio.wav"))
        extract_audio_from_video(video_path, audio_path)

        # Step 2: Transcribe the audio to text
        transcribed_text = transcribe_audio(audio_path)
        print("Transcribed Text:", transcribed_text)

        # Step 3: Translate the text to the target language
        translated_text = translate_text(transcribed_text, target_language)
        print("Translated Text:", translated_text)

        # Step 4: Convert the translated text to speech
        dubbed_audio_path = os.path.join(DUBBED_VIDEO_DIR, os.path.basename(video_path).replace(".mp4", f"_dubbed_{target_language}.wav"))
        text_to_speech(translated_text, target_language, dubbed_audio_path)

        # Step 5: Merge the dubbed audio with the original video
        dubbed_video_path = os.path.join(DUBBED_VIDEO_DIR, os.path.basename(video_path).replace(".mp4", f"_dubbed_{target_language}.mp4"))
        merge_audio_with_video(video_path, dubbed_audio_path, dubbed_video_path)

        # Clean up temporary files
        os.remove(audio_path)
        os.remove(dubbed_audio_path)

        print(f"Dubbed video saved at: {dubbed_video_path}")
        return dubbed_video_path

    except Exception as e:
        print(f"Error during dubbing: {str(e)}")
        raise e
