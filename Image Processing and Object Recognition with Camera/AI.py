import cv2
import numpy as np
import tensorflow as tf

# Model yükleme
model = tf.keras.applications.MobileNetV2(weights='imagenet')

# Kamera başlatma
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Görüntüyü hazırlama
    img = cv2.resize(frame, (224, 224))
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)

    # Tahmin
    preds = model.predict(img)
    label = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)[0][0][1]
    
    # Görüntüyü ekranda gösterme
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
