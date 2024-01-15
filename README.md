# Compressione-dati
We are attempting to create a project in which, given a specific video, faces are obscured wherever they are present, and the processed video is returned as output. 
All of this is being developed in Python using OpenCV and dlib.

Istruzioni:
Eseguire il file Main.py con la directory del video come argomento.
```
python Main.py path/to/input_video.mp4
```
Il programma cerca una cartella training, dove sono presenti le immagini dei volti conosciuti, e una cartella immagini_per_sostituzione, dove sono presenti i volti da utilizzare per la sostituzione. Per un esempio, si veda la cartella https://github.com/cfederico14/Compressione-dati/tree/modifiche/esempio
Aggiungere -a come argomento sostituisce tutti i volti presenti nell'immagine, rimpiazzando i volti sconosciuti con l'immagine volto_sconosciuto.jpg presente nella directory del video.
```
python Main.py path/to/input_video.mp4 -a
```
