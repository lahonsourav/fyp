import streamlit as st

st.title("AVSR")

# Add video upload functionality
uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

if uploaded_video is not None:
    st.video(uploaded_video)
    st.success("Video uploaded successfully!")