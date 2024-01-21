import face_recognition
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import os
import shutil
from pathlib import Path

def estrai_volto_da_immagine(volto_da_estrarre_path):
    # Carica l'immagine contenente il volto da estrarre
    immagine = face_recognition.load_image_file(volto_da_estrarre_path)
    
    # Codifica il volto da estrarre
    volto_da_estrarre = face_recognition.load_image_file(volto_da_estrarre_path)
    codifica_volto_da_estrarre = face_recognition.face_encodings(volto_da_estrarre)[0]

    # Trova tutti i volti nell'immagine
    face_locations = face_recognition.face_locations(immagine)
    codifiche_volto_immagine = face_recognition.face_encodings(immagine, face_locations)
    pil_image = None

    for codifica_volto in codifiche_volto_immagine:
        # Confronta la codifica del volto estratto con la codifica del volto dall'immagine
        confronto = face_recognition.compare_faces([codifica_volto_da_estrarre], codifica_volto)

        if confronto[0]:
            # Estrai il volto dall'immagine
            top, right, bottom, left = face_recognition.face_locations(immagine)[0]
            face_image = immagine[top:bottom, left:right]

            # Converti l'array NumPy in un oggetto immagine di PIL
            pil_image = Image.fromarray(face_image)

    return pil_image

def esegui_sostituzione(video_frame_folder, training_folder, sub_images_folder, output_folder, generic_image_path = ""):

    # Assicurati che la cartella di output esista, altrimenti creala

    if(os.path.exists(output_folder)):
        try:
            path = Path(output_folder)
            shutil.rmtree(path)
            print("Cartella eliminata")
        except OSError as o:
            print(f"Error, {o.strerror}: {path}")

    os.makedirs(output_folder, exist_ok=True)

    # Crea gli array per i volti conosciuti
    training_images_array = []
    known_face_encodings = []
    known_face_names = []
    dir = os.listdir(training_folder)
    if len(dir) > 0:
        for filename in dir:
            if filename.endswith(".jpg") or filename.endswith(".png"):
                img = face_recognition.load_image_file(os.path.join(training_folder, filename))
                training_images_array.append(img)
                face_encoding = face_recognition.face_encodings(img)[0]
                known_face_encodings.append(face_encoding)
                face_name = Path(filename).stem
                known_face_names.append(face_name)

    # Assegna ad ogni volto conosciuto un'immagine da utilizzare per la sostituzione tramite un dizionario
    faces_for_substitution = []
    for f in os.listdir(sub_images_folder):
        if f.endswith(".jpg") or f.endswith(".png"):
            faces_for_substitution.append(f)

    faces_dictionary = {}
    index = 0;
    for face_name in known_face_names:
        # Se ci sono piú facce conosciute che facce per la sostituzione, riutilizza le immagini partendo da 0
        sub_image_path = os.path.join(sub_images_folder, faces_for_substitution[index % len(faces_for_substitution)])
        faces_dictionary[face_name] = estrai_volto_da_immagine(sub_image_path)
        index += 1

    generic_image = None
    if(generic_image_path != ""):
        generic_image = Image.open(generic_image_path)
    # Load a sample picture and learn how to recognize it.
    # Cicla attraverso tutte le immagini nella cartella di input
    for filename in os.listdir(video_frame_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(video_frame_folder, filename)
            print(image_path)

            # Load an image with an unknown face
            unknown_image = face_recognition.load_image_file(image_path)

            # Find all the faces and face encodings in the unknown image
            face_locations = face_recognition.face_locations(unknown_image)
            face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

            # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
            # See http://pillow.readthedocs.io/ for more about PIL/Pillow
            pil_image = Image.fromarray(unknown_image)
            # Create a Pillow ImageDraw Draw instance to draw with
            draw = ImageDraw.Draw(pil_image)
            #pil_image.show()
            # Loop through each face found in the unknown image
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # See if the face is a match for the known face(s)
                name = "Unknown"

                # Necessario per il funzionamento in caso di sostituzione di tutte le facce senza facce da identificare
                if len(known_face_encodings) > 0:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                print(name)

                # Controlla se la faccia trovata corrisponde a qualcuno da indentificare
                if name in faces_dictionary:
                    myimage = faces_dictionary[name]
                # Se la faccia trovata non corrisponde a nessuno e il programma ha arg -a sostituisci con immagine generica
                elif name == "Unknown":
                    if(generic_image != None):
                        myimage = generic_image
                else:
                    break


                volto_ritagliato = pil_image.crop((left, top, right, bottom))
                volto_ritagliato.convert("RGBA")
                myimage = myimage.resize((volto_ritagliato.size))
                myimage.convert("RGBA")
                volto_ritagliato.paste(myimage)
                pil_image.paste(volto_ritagliato,(left, top, right, bottom))

            file_name = os.path.splitext(os.path.basename(image_path))[0]
            # Crea il percorso per salvare l'immagine modificata
            output_path = os.path.join(output_folder, f"{file_name}_modified.png")
            # You can also save a copy of the new image to disk if you want by uncommenting this line
            pil_image.save(output_path)
