import streamlit as st
import os
import subprocess
import uuid
import speech_recognition as sr

st.title("AVSR - Automatic Video Speech Recognition")

uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

if uploaded_video is not None:
    st.video(uploaded_video)

    unique_id = str(uuid.uuid4())
    video_path = f"temp_{unique_id}.mp4"
    audio_path = f"temp_{unique_id}.wav"

    with open(video_path, "wb") as f:
        f.write(uploaded_video.read())

    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1", audio_path
    ]
    try:
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        st.error("Failed to extract audio from the video.")
    else:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                st.write(text)
            except sr.UnknownValueError:
                st.write("Could not understand the audio.")
            except sr.RequestError as e:
                st.write(f"Speech recognition failed: {e}")

    os.remove(video_path)
    os.remove(audio_path)
