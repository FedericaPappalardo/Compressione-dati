import subprocess
import os

def estrai_audio(video_input, output_folder):
    # Crea una sottocartella per contenere l'audio
    output_subfolder = output_folder
    os.makedirs(output_subfolder, exist_ok=True)

    output_path = os.path.join(output_subfolder, 'audio.mkv')

    comando = [
        'ffmpeg',
        '-i', video_input,
        '-vn',  # Specifica che non vuoi video, solo audio
        '-y',
        '-c:a', 'copy',  # Specifica il codec audio per il salvataggio come MP3
        output_path
    ]

    subprocess.run(comando)

def dividere_in_frame(video_input, output_folder, output_pattern='frame_%04d.png', fps=1):
    # Estrai l'audio prima di dividere il video
    estrai_audio(video_input, output_folder)

    # Crea una sottocartella per contenere le immagini
    output_subfolder = output_folder
    os.makedirs(output_subfolder, exist_ok=True)

    # Si dovrebbero eliminare i file giá presenti nella cartella

    output_path = os.path.join(output_subfolder, output_pattern)

    comando = [
        'ffmpeg',
        '-i', video_input,
        '-q:v', '2',
        output_path
    ]

    subprocess.run(comando)

def get_framerate(video_input):
    comando = [
        'ffprobe',
        '-v', '0',
        '-of', 'csv=p=0',
        '-select_streams',
        'v:0',
        '-show_entries', 'stream=r_frame_rate',
        video_input
    ]

    if ".mpg" in video_input:
        framerate = "25"
    else:
        result = subprocess.run(comando, capture_output = True, text = True)
        framerate = result.stdout
    print("Il framerate rilevato é: ", framerate)
    return framerate
