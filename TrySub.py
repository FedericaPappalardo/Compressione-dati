import os
import cv2
import dlib
from imutils import face_utils

# Carica il classificatore per il rilevamento del volto di OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Carica il modello di predizione dei landmarks di Dlib
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Funzione per estrarre il volto da un'immagine
def extract_face_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Rileva i volti utilizzando il classificatore di OpenCV
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Se viene rilevato almeno un volto, estrai il primo
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        face = image[y:y + h, x:x + w]
        return face
    else:
        return None

# Funzione per sostituire il volto con un'immagine
def replace_face_with_image(frame, face, replacement_face):
    (x, y, w, h) = face

    # Calcola la scala dell'immagine sostitutiva in base alle dimensioni del volto nel frame
    scale_factor_x = w / replacement_face.shape[1]
    scale_factor_y = h / replacement_face.shape[0]

    # Ridimensiona l'immagine sostitutiva in modo proporzionale
    replacement_face_resized = cv2.resize(replacement_face, None, fx=scale_factor_x, fy=scale_factor_y)

    # Calcola la posizione per sovrapporre l'immagine sostitutiva sul volto nel frame
    x_offset = x
    y_offset = y

    # Sovrappone l'immagine sostitutiva al volto nel frame
    frame[y_offset:y_offset + replacement_face_resized.shape[0], x_offset:x_offset + replacement_face_resized.shape[1]] = replacement_face_resized

    return frame


# Funzione per individuare i volti e sostituire ciascun volto con un volto preso da un'immagine specifica
def replace_faces_and_save(image_path, output_folder, replacement_image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Rileva i volti utilizzando il classificatore di OpenCV
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Estrai il volto dalla seconda immagine
    replacement_face = extract_face_from_image(replacement_image_path)

    if replacement_face is not None:
        for face in faces:
            # Sostituisci il volto nel frame con il volto estratto dall'immagine sostitutiva
            image = replace_face_with_image(image, face, replacement_face)

        # Ottieni il nome del file senza estensione
        file_name = os.path.splitext(os.path.basename(image_path))[0]

        # Crea il percorso per salvare l'immagine modificata
        output_path = os.path.join(output_folder, f"{file_name}_modified.jpg")

        # Salva l'immagine modificata nella nuova cartella
        cv2.imwrite(output_path, image)
    else:
        print(f"Nessun volto rilevato in {replacement_image_path}")

# Sostituisci "input_folder" con il percorso della cartella contenente le immagini da elaborare
input_folder = "C:\\Users\\carmi\\Desktop\\Compressione dati\\frame_images"

# Sostituisci "output_folder" con il percorso della nuova cartella in cui salvare le immagini modificate
output_folder = "C:\\Users\\carmi\\Desktop\\Compressione dati\\frame_modificati"

# Sostituisci "replacement_image_path" con il percorso dell'immagine da
#  utilizzare come sostituto per il volto
replacement_image_path = "C:\\Users\\carmi\\Downloads\\Luca-transformed.png"

# Assicurati che la cartella di output esista, altrimenti creala
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Cicla attraverso tutte le immagini nella cartella di input
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(input_folder, filename)
        replace_faces_and_save(image_path, output_folder, replacement_image_path)
