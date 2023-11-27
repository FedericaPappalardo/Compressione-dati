import subprocess
import os
import TryFFMPEG

def ricomporre_video_da_frame(frames_folder, audio_file, output_path, framerate = 30):
    # Assicurati che la cartella di output esista, altrimenti creala
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    comando = [
        'C:\\Users\\carmi\\Desktop\\Compressione dati\\ffmpeg-2023-11-22-git-0008e1c5d5-full_build\\ffmpeg-2023-11-22-git-0008e1c5d5-full_build\\bin\\ffmpeg.exe',
        '-framerate', framerate,  # Sostituisci con l'fps corretto, da ottenere tramite la funzione get_framerate
        '-i', os.path.join(frames_folder, 'frame_%04d_modified.jpg'),  # Sostituisci con il pattern corretto
        '-i', audio_file,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-b:a', '192k',
        '-shortest',
        output_path
    ]

    subprocess.run(comando)

# Esempio di utilizzo
frames_folder = 'C:\\Users\\carmi\\Desktop\\Compressione dati\\frame_modificati'
audio_file = 'C:\\Users\\carmi\\Desktop\\Compressione dati\\Estratto_audio_video\\audio.mp3'
output_video = 'C:\\Users\\carmi\\Desktop\\Compressione dati\\video_finale.mp4'

ricomporre_video_da_frame(frames_folder, audio_file, output_video)
