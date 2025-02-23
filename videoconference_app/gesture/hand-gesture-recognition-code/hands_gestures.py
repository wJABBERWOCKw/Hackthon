
from django.shortcuts import render
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
model = load_model('mp_hand_gesture')

# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)


# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
# Read each frame from the webcam
    _, frame = cap.read()

    x, y, c = frame.shape

# Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Get hand landmark prediction
    result = hands.process(framergb)

# print(result)

    className = ''

# post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
            # print(id, lm)
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)

                landmarks.append([lmx, lmy])

        # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

        # Predict gesture
            prediction = model.predict([landmarks])
        # print(prediction)
            classID = np.argmax(prediction)
            className = classNames[classID]

# show the prediction on the frame
        cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
               1, (0,0,255), 2, cv2.LINE_AA)
        #_, jpeg_frame = cv2.imencode('.jpg', frame)
       # yield (b'--frame\r\n'
              # b'Content-Type: image/jpeg\r\n\r\n' + jpeg_frame.tobytes() + b'\r\n')
# Show the final output
    cv2.imshow("Output", frame)

    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
cap.release()

cv2.destroyAllWindows()


# import cv2
# import numpy as np
# import mediapipe as mp
# import tensorflow as tf
# from tensorflow.keras.models import load_model
#
# # Initialize mediapipe
# mpHands = mp.solutions.hands
# hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
# mpDraw = mp.solutions.drawing_utils
#
# # Load the gesture recognizer model
# model = load_model('mp_hand_gesture')
#
# # Load class names
# with open('gesture.names', 'r') as f:
#     classNames = f.read().split('\n')
#
# def perform_gesture_prediction():
#     cap = cv2.VideoCapture(0)
#
#     while True:
#         _, frame = cap.read()
#
#         x, y, c = frame.shape
#         frame = cv2.flip(frame, 1)
#         framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#         result = hands.process(framergb)
#
#         className = ''
#
#         if result.multi_hand_landmarks:
#             landmarks = []
#             for handslms in result.multi_hand_landmarks:
#                 for lm in handslms.landmark:
#                     lmx = int(lm.x * x)
#                     lmy = int(lm.y * y)
#                     landmarks.append([lmx, lmy])
#
#                 mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
#
#                 prediction = model.predict([landmarks])
#                 classID = np.argmax(prediction)
#                 className = classNames[classID]
#
#             cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
#                         1, (0, 0, 255), 2, cv2.LINE_AA)
#
#             _, jpeg_frame = cv2.imencode('.jpg', frame)
#             frame_bytes = jpeg_frame.tobytes()
#
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
#
#             if cv2.waitKey(1) == ord('q'):
#                 break
#
#     cap.release()
#     cv2.destroyAllWindows()


