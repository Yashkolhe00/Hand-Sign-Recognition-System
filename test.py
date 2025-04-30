import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import pyttsx3

engine = pyttsx3.init()

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
offset = 20
imgSize = 300

with open("Model/labels.txt", "r") as f:
    labels = [line.strip().split(' ')[-1] for line in f.readlines()]  # Takes the last word as label

last_gesture = None

while True:
    success, img = cap.read()
    if not success:
        continue

    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

            try:
                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize

                prediction, index = classifier.getPrediction(imgWhite, draw=False)

                if index < len(labels):
                    predicted_label = labels[index]
                    confidence = prediction[index]
                    print(f"Predicted: {predicted_label}, Confidence: {confidence}")

                    # Only speak if confidence > 80% and different from last gesture
                    if predicted_label != last_gesture and confidence > 0.8:
                        engine.say(predicted_label)
                        engine.runAndWait()
                        last_gesture = predicted_label

                    # Display the clean label without any prefixes
                    cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                                  (x - offset + 200, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
                    cv2.putText(imgOutput, f"{predicted_label} {confidence:.2f}",
                                (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), 2)
                    cv2.rectangle(imgOutput, (x - offset, y - offset),
                                  (x + w + offset, y + h + offset), (255, 0, 255), 4)

            except Exception as e:
                print(f"Error processing hand: {e}")

    cv2.imshow("Sign Language Detection", imgOutput)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()