import cv2
import os

def crea_video(cartella_immagini, percorso_output_video, fps=30):
    # Ottieni la lista di file nella cartella delle immagini
    elenco_immagini = [img for img in os.listdir(cartella_immagini) if img.endswith(".jpg")]
    elenco_immagini.sort()  # Ordina le immagini in modo da essere nel giusto ordine temporale

    # Ottieni le dimensioni dell'immagine dal primo frame
    img = cv2.imread(os.path.join(cartella_immagini, elenco_immagini[0]))
    altezza, larghezza, _ = img.shape

    # Specifica il codec video e crea l'oggetto VideoWriter
    # Specifica il codec video e crea l'oggetto VideoWriter
    codec = cv2.VideoWriter_fourcc(*"mp4v")  # Puoi cambiare il codec a seconda delle tue esigenze

    # Usa un modello di nome file con un segnaposto per il numero del frame (ad esempio, %d)
    percorso_output_video = "C:\\Users\\carmi\\Desktop\\Compressioni\\percorso_cartella_output\\video_output.mp4"
    video = cv2.VideoWriter(percorso_output_video, codec, fps, (larghezza, altezza))

    # Aggiungi ciascun frame al video
    for indice, immagine in enumerate(elenco_immagini):
        percorso_immagine = os.path.join(cartella_immagini, immagine)
        frame = cv2.imread(percorso_immagine)

        # Assicurati che il frame sia valido
        if frame is not None:
            # Aggiungi il numero del frame al nome del file di output
            nome_frame = f"frame_{str(indice + 1).zfill(4)}.png"
            video.write(frame)

    # Rilascia l'oggetto VideoWriter
    video.release()

# Esempio di utilizzo
img_path = 'C:\\Users\\carmi\\Desktop\\Compressioni\\percorso_cartella_output'
video_path = 'C:\\Users\\carmi\\Desktop\\Compressioni\\percorso_cartella_output'
# Esempio di utilizzo
crea_video(img_path, video_path)
