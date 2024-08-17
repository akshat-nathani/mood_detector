import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model


model = load_model("facialemotionmodel.h5")


haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)


def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)  # Reshape to match model's expected input
    return feature / 255.0  # Normalize the input


webcam = cv2.VideoCapture(0)


labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

while True:
 
    ret, im = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)  
    
 
    for (p, q, r, s) in faces:
        image = gray[q:q+s, p:p+r] 
        cv2.rectangle(im, (p, q), (p+r, q+s), (255, 0, 0), 2)  
        image = cv2.resize(image, (48, 48))  
        img = extract_features(image)  
        pred = model.predict(img)  
        prediction_label = labels[pred.argmax()]
        cv2.putText(im, prediction_label, (p-10, q-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))  
    
 
    cv2.imshow("Output", im)
    
    
    if cv2.waitKey(27) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
