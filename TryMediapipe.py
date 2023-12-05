import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

my_drawing_specs = mp_drawing.DrawingSpec(color = (0, 255, 0), thickness = 1)
video_input = "PATH_TO_INPUT_VIDEO"
cap = cv2.VideoCapture(video_input)
if cap.isOpened() == False:
    print("Errore nell'apertura del video")
    raise TypeError

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
video_output = "PATH_TO_OUTPUT_VIDEO"
out = cv2.VideoWriter(video_output, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 60, (frame_width, frame_height))

mp_face_mesh = mp.solutions.face_mesh

with mp_face_mesh.FaceMesh(
        max_num_faces = 2,
        refine_landmarks = True,
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.5
    ) as face_mesh:
    

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break
            
            
        results = face_mesh.process(image)

        if not results.multi_face_landmarks:
            continue
        
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image = image,
                landmark_list = face_landmarks,
                connections = mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec = None,
                connection_drawing_spec = mp_drawing_styles
                .get_default_face_mesh_tesselation_style()
            )
            
            mp_drawing.draw_landmarks(
                image = image,
                landmark_list = face_landmarks,
                connections = mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec = None,
                connection_drawing_spec = my_drawing_specs
#                 .get_default_face_mesh_contours_style()
            )


        #cv2.imshow("My video capture", cv2.flip(image, 1))
        cv2.imshow("My video capture", image)
        out.write(image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()
