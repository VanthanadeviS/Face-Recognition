import face_recognition
import cv2
import numpy as np
import time
from datetime import datetime
now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
timehr = now.strftime("%H %M %S")
whole = day + month + year

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
krish_image = face_recognition.load_image_file("sathiya/Sathiya.jpg")
krish_face_encoding = face_recognition.face_encodings(krish_image)[0]

# Load a second sample picture and learn how to recognize it.
bradley_image = face_recognition.load_image_file("Bradley/bradley.jpeg")
bradley_face_encoding = face_recognition.face_encodings(bradley_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    krish_face_encoding,
    bradley_face_encoding
]
known_face_names = [
    "sathiya",
    "Bradley"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
currentframe = 0

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names =[]
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            print(matches[0])
            print(matches[1])

            # if name == "Unknown":
            #     time.sleep(5)
            #     name1 = './data/frame' + str(currentframe) + '.jpg'
            #     print('Creating...' + name1)
            #
            #     # writing the extracted images
            #     cv2.imwrite(name1, frame)
            #
            #     # increasing counter so that it will
            #     # show how many frames are created
            #     currentframe += 1
            # else:
            #     pass

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                # print(name+ "sdfs")
                # print(matches[best_match_index])
            face_names.append(name)
    elif(matches[0] == False and matches[1] == False):
        # print(matches[0])
        # print(matches[1])
        print("hello11")
        time.sleep(5)
        name1 = './data/image'+ day +" "+ month +" "+ year +"  "+ timehr + "  " +  str(currentframe) + '.jpg'
        print('Creating...' + name1)

        # writing the extracted images
        cv2.imwrite(name1, frame)

        # increasing counter so that it will
        # show how many frames are created
        currentframe += 1
            # print(face_names)



    #process_this_frame = not process_this_frame



    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)


    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
