'''import cv2
import os

# Percorso della cartella contenente i frame del video
frame_folder_path = "C:\\Users\\carmi\\Desktop\\Compressione dati\\frame_modificati"

# Percorso del file audio del video
audio_file_path = "C:\\Users\\carmi\\Desktop\\Compressione dati\\Estratto_audio_video\\audio.mp3"

# Output: Percorso e nome del video da generare
output_video_path = "C:\\Users\\carmi\\Desktop\\Compressione dati\\video_finale.mp4"

# Inizializza il VideoWriter per scrivere il nuovo video
frame = cv2.imread(os.path.join(frame_folder_path, os.listdir(frame_folder_path)[0]))
height, width, layers = frame.shape
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video_writer = cv2.VideoWriter(output_video_path, fourcc, 30, (width, height))

# Leggi ogni frame dalla cartella e scrivilo nel video
for filename in sorted(os.listdir(frame_folder_path)):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        frame_path = os.path.join(frame_folder_path, filename)
        frame = cv2.imread(frame_path)
        video_writer.write(frame)

# Rilascia le risorse del VideoWriter
video_writer.release()

# Aggiungi l'audio al video
os.system(f"ffmpeg -i {output_video_path} -i {audio_file_path} -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 {output_video_path}_with_audio.mp4")
'''

import subprocess
import os

def ricomporre_video_da_frame(frames_folder, audio_file, output_path):
    # Assicurati che la cartella di output esista, altrimenti creala
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    comando = [
        'C:\\Users\\carmi\\Desktop\\Compressione dati\\ffmpeg-2023-11-22-git-0008e1c5d5-full_build\\ffmpeg-2023-11-22-git-0008e1c5d5-full_build\\bin\\ffmpeg.exe',
        '-framerate', '30',  # Sostituisci con l'fps corretto
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
