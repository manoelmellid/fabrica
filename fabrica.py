import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def split_video(video_path, chunk_length=180):
    """Divide el video en fragmentos de la duración especificada."""
    clips = []
    video = VideoFileClip(video_path)
    duration = int(video.duration)
    
    for start in range(0, duration, chunk_length):
        end = min(start + chunk_length, duration)
        clip = video.subclip(start, end)
        clip_path = f"output_part_{start//chunk_length + 1}.mp4"
        clip.write_videofile(clip_path, codec="libx264", audio_codec="aac")
        clips.append(clip_path)
    
    return clips

st.title("Divisor de Videos MP4")

uploaded_file = st.file_uploader("Sube un archivo MP4", type=["mp4"])

if uploaded_file is not None:
    temp_video_path = "temp_video.mp4"
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.write("Dividiendo el video en fragmentos de 3 minutos...")
    output_files = split_video(temp_video_path)
    
    for file in output_files:
        st.video(file)
        with open(file, "rb") as f:
            st.download_button("Descargar", f, file, mime="video/mp4")
    
    os.remove(temp_video_path)
    for file in output_files:
        os.remove(file)
