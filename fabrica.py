import streamlit as st
import os
import gdown
import zipfile
from moviepy.video.io.VideoFileClip import VideoFileClip

st.title("Procesar y dividir videos MP4")

# Función para dividir el video en fragmentos de 3 minutos (180 segundos)
# Función para dividir el video en fragmentos de 3 minutos (180 segundos)
def split_video_ffmpeg(input_video):
    output_pattern = "output_part_%03d.mp4"
    cmd = f"ffmpeg -i {input_video} -c copy -map 0 -segment_time 180 -f segment -reset_timestamps 1 {output_pattern}"
    os.system(cmd)
    
    # Obtener los archivos generados
    output_files = [f"output_part_{i:03d}.mp4" for i in range(1, len(os.listdir()) + 1) if f"output_part_{i:03d}.mp4" in os.listdir()]
    return output_files
    
split_video_ffmpeg("downloaded_video.mp4")

# Función para crear un ZIP con los fragmentos
def create_zip(output_files, zip_name="videos_divididos.zip"):
    with zipfile.ZipFile(zip_name, "w") as zipf:
        for file in output_files:
            zipf.write(file, os.path.basename(file))
    return zip_name

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
# Procesar el video si se ha subido o descargado uno
if video_path:
    st.write("Procesando el video... Esto puede tardar unos minutos.")
    
    output_files = split_video_ffmpeg(video_path)  # Cambiar de split_video a split_video_ffmpeg

    if output_files:
        zip_path = create_zip(output_files)
        with open(zip_path, "rb") as zipf:
            st.download_button("Descargar todos los clips", zipf, file_name=zip_path, mime="application/zip")
        
        # Limpiar archivos temporales
        os.remove(video_path)
        for file in output_files:
            os.remove(file)
        os.remove(zip_path)
