import cv2
import os

# Percorso al video
video_path = 'C:\\Users\\carmi\\Downloads\\prova.mp4'

# Apri il video
cap = cv2.VideoCapture(video_path)

# Verifica se il video è aperto correttamente
if not cap.isOpened():
    print("Errore nell'apertura del video.")
    exit()

# Percorso per salvare le immagini
cartella_immagini = 'immagini_da_video'
os.makedirs(cartella_immagini, exist_ok=True)

# Loop per l'estrazione delle immagini
count = 0
while True:
    # Leggi il frame dal video
    ret, frame = cap.read()

    # Verifica se il video è finito
    if not ret:
        break

    # Salva il frame come immagine
    image_name = f'frame_{count:04d}.png'
    image_path = os.path.join(cartella_immagini, image_name)
    cv2.imwrite(image_path, frame)

    # Incrementa il contatore
    count += 1

# Rilascia le risorse
cap.release()

print(f"Immagini estratte con successo nella cartella: {cartella_immagini}")
