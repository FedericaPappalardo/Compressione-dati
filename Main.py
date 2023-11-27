#!/usr/bin/env python3

import sys
import TryFFMPEG, TrySub, TryRebuildVideo

def main(input_video, output_folder, replacement_image_path):
    # TryFFMPEG.estrai_audio(input_video, output_folder)
    TryFFMPEG.dividere_in_frame(input_video, output_folder)

    for filename in os.listdir(output_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(input_folder, filename)
            TrySub.replace_faces_and_save(image_path, output_folder, replacement_image_path)

    audio_file = os.path.join(output_folder, "audio.mp3")
    output_video = os.path.join(output_folder, "output_video.mp4")
    framerate = TryFFMPEG.get_framerate(input_video)

    TryRebuildVideo.ricomporre_video_da_frame(output_folder, audio_file, output_folder, framerate)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Errore! uso: Main.py input_video output_folder replacement_image_path")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
