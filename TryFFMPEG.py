import subprocess
import os
video_input = 'C:\\Users\\carmi\\Downloads\\prova.mp4'
output_folder ='C:\\Users\\carmi\\Desktop\\Compressione dati'
def estrai_audio(video_input, output_folder):
    # Crea una sottocartella per contenere l'audio
    output_subfolder = os.path.join(output_folder, 'Estratto_audio_video')
    os.makedirs(output_subfolder, exist_ok=True)

    output_path = os.path.join(output_subfolder, 'audio.mp3')

    comando = [
        'C:\\Users\\carmi\\Desktop\\Compressione dati\\ffmpeg-2023-11-22-git-0008e1c5d5-full_build\\ffmpeg-2023-11-22-git-0008e1c5d5-full_build\\bin\\ffmpeg.exe',
        '-i', video_input,
        '-vn',  # Specifica che non vuoi video, solo audio
        '-acodec', 'libmp3lame',  # Specifica il codec audio per il salvataggio come MP3
        output_path
    ]

    subprocess.run(comando)

def dividere_in_frame(video_input, output_folder, output_pattern='frame_%04d.jpg', fps=1):
    # Estrai l'audio prima di dividere il video
    estrai_audio(video_input, output_folder)

    # Crea una sottocartella per contenere le immagini
    output_subfolder = os.path.join(output_folder, 'frame_images')
    os.makedirs(output_subfolder, exist_ok=True)

    output_path = os.path.join(output_subfolder, output_pattern)

    comando = [
        'C:\\Users\\carmi\\Desktop\\Compressione dati\\ffmpeg-2023-11-22-git-0008e1c5d5-full_build\\ffmpeg-2023-11-22-git-0008e1c5d5-full_build\\bin\\ffmpeg.exe',
        '-i', video_input,
        '-vf', f'fps={fps}',
        '-q:v', '2',
        output_path
    ]

    subprocess.run(comando)

# Esempio di utilizzo
dividere_in_frame(video_input, output_folder, fps=1)
