import streamlit as st
import os
import gdown
from moviepy.video.io.VideoFileClip import VideoFileClip

st.title("Procesar y dividir videos MP4")

# Función para dividir el video
def split_video(video_path, chunk_length=180):
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

# Opción 1: Subir archivo manualmente
uploaded_file = st.file_uploader("Sube un archivo MP4", type=["mp4"])

# Opción 2: Descargar desde Google Drive
video_url = st.text_input("O pega un enlace de Google Drive (asegúrate de que sea público):")

video_path = None  # Para almacenar la ruta del video

if video_url:
    try:
        file_id = video_url.split("/d/")[1].split("/")[0]
        download_url = f"https://drive.google.com/uc?id={file_id}"
        video_path = "downloaded_video.mp4"
        gdown.download(download_url, video_path, quiet=False)
        st.success("¡Video descargado con éxito!")
    except Exception as e:
        st.error("Error al descargar el video. Verifica el enlace.")

elif uploaded_file is not None:
    video_path = "uploaded_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

# Procesar el video si se ha subido o descargado uno
if video_path:
    st.video(video_path)
    st.write("Dividiendo el video en fragmentos de 3 minutos...")
    
    output_files = split_video(video_path)
    
    for file in output_files:
        st.video(file)
        with open(file, "rb") as f:
            st.download_button(f"Descargar {file}", f, file, mime="video/mp4")

    # Eliminar archivos temporales
    os.remove(video_path)
    for file in output_files:
        os.remove(file)
