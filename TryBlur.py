import os
import cv2
import dlib
from imutils import face_utils

# Carica il classificatore per il rilevamento del volto di OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Carica il modello di predizione dei landmarks di Dlib
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Funzione per applicare l'effetto di sfocatura a una regione dell'immagine
def apply_blur(image, face):
    (x, y, w, h) = face
    roi = image[y:y + h, x:x + w]
    blurred_roi = cv2.GaussianBlur(roi, (99, 99), 10)
    image[y:y + h, x:x + w] = blurred_roi
    return image


# Funzione per individuare i volti, applicare l'effetto di sfocatura e salvare le immagini modificate
def blur_faces_and_save(image_path, output_folder):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    

    # Rileva i volti utilizzando il classificatore di OpenCV
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for face in faces :
        # Utilizza Dlib per ottenere i landmarks facciali
        rect = dlib.rectangle(int(face[0]), int(face[1]), int(face[0] + face[2]), int(face[1] + face[3]))
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        # Applica l'effetto di sfocatura alla regione del volto utilizzando i landmarks
        image = apply_blur(image, (face[0], face[1], face[2], face[3]))

    # Ottieni il nome del file senza estensione
    file_name = os.path.splitext(os.path.basename(image_path))[0]

    # Crea il percorso per salvare l'immagine sfocata
    output_path = os.path.join(output_folder, f"{file_name}_blurred.jpg")

    # Salva l'immagine sfocata nella nuova cartella
    cv2.imwrite(output_path, image)

# Sostituisci "input_folder" con il percorso della cartella contenente le immagini da elaborare
input_folder = "C:\\Users\\carmi\\Desktop\\Compressioni\\immagini_da_video"

# Sostituisci "output_folder" con il percorso della nuova cartella in cui salvare le immagini sfocate
output_folder = "percorso_cartella_output"

# Assicurati che la cartella di output esista, altrimenti creala
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Cicla attraverso tutte le immagini nella cartella di input
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(input_folder, filename)
        #image_path = image_path.replace( "\\" , "\\\\" )
        blur_faces_and_save(image_path, output_folder)
    
