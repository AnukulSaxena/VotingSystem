import imutils
import dlib
import cv2
import numpy as np
import face_recognition
from scipy.spatial import distance
from imutils import face_utils
from imutils.video import WebcamVideoStream
from vote import*


def abc():
    known_image = face_recognition.load_image_file("anukul.png")
    known_encoding = face_recognition.face_encodings(known_image)[0]
    face_locations = []
    face_encodings = []
    face_names = []
    detect = dlib.get_frontal_face_detector()
    predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code
    vs = WebcamVideoStream(src=0).start()
    #count = 1
    for i in range(1):
        input=vs.read()
        gray = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
        subjects = detect(gray, 0)
        frame = cv2.resize(gray, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces([known_encoding], face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = "Known Person"
                face_names.append(name)
                cv2.imshow("Frame", input)
                if name == "Known Person":
                    print("vote")
                    #count = count+1
                    #root = Tk()
                    #application = atm(root)
                    vote()
        #else:      
         #   break
                    #root.mainloop()     
            #break
            vs.stop()
            cv2.destroyAllWindows()

