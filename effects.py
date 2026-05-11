import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def render_frame(frame, attiva):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    if not attiva:
        # Se la sfocatura è spenta, ritorniamo il frame originale e il numero di facce
        return frame, len(faces)

    # Se attiva, applichiamo la sfocatura selettiva
    blurred = cv2.GaussianBlur(frame, (95, 95), 0)
    for (x, y, w, h) in faces:
        blurred[y:y + h, x:x + w] = frame[y:y + h, x:x + w]
        cv2.rectangle(blurred, (x, y), (x + w, y + h), (0, 255, 0), 1)

    return blurred, len(faces)