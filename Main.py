#!/usr/bin/env python3

import sys
import os
import TryFFMPEG
import TryRebuildVideo
import TrySub

def main(input_video):

    frame_folder = os.path.join(os.path.dirname(input_video), "extracted_frames")
    TryFFMPEG.dividere_in_frame(input_video, frame_folder)

    sub_frame_folder = os.path.join(os.path.dirname(input_video), "substituted_frames")
    training_folder = os.path.join(os.path.dirname(input_video), "training")
    imm_sost_folder = os.path.join(os.path.dirname(input_video), "immagini_per_sostituzione")
    TrySub.esegui_sostituzione(frame_folder, training_folder, imm_sost_folder, sub_frame_folder)

    audio_file = os.path.join(frame_folder, "audio.mp3")
    output_video = os.path.join(os.path.dirname(input_video), "output_video.mp4")
    framerate = TryFFMPEG.get_framerate(input_video)

    TryRebuildVideo.ricomporre_video_da_frame(sub_frame_folder, audio_file, output_video, framerate)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Errore! uso: Main.py input_video")
    else:
        main(sys.argv[1])
