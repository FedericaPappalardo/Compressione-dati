import subprocess
import os
import TryFFMPEG

def ricomporre_video_da_frame(frames_folder, audio_file, output_path, framerate = '25'):
    # Assicurati che la cartella di output esista, altrimenti creala
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    frames_path = frames_folder

    comando = [
        'ffmpeg',
        '-framerate', framerate,  # Sostituisci con l'fps corretto, da ottenere tramite la funzione get_framerate
        '-i', os.path.join(frames_path, 'frame_%04d_modified.jpg'),  # Sostituisci con il pattern corretto
        '-c:v', 'libx264',
        '-c:a', 'copy',
        '-y',
        '-shortest',
        output_path
    ]

    if os.path.exists(audio_file):
        comando += ["-i", audio_file]

    subprocess.run(comando)
