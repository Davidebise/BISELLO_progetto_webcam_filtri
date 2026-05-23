import cv2
import numpy as np
import os

# Inizializzazione dei classificatori
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


def carica_asset(path):
    if os.path.exists(path):
        return cv2.imread(path, cv2.IMREAD_UNCHANGED)
    return None


cappello_img = carica_asset("cappello.png")
occhiali_img = carica_asset("occhiali.png")
barba_img = carica_asset("barba.png")


def sovrapponi_png(sfondo, img_png, x, y, w, h):
    if img_png is None:
        return sfondo

    img_res = cv2.resize(img_png, (w, h), interpolation=cv2.INTER_AREA)

    if img_res.shape[2] == 3:
        alpha_artificiale = np.ones((img_res.shape[0], img_res.shape[1]), dtype=np.uint8) * 255
        img_res = cv2.merge([img_res[:, :, 0], img_res[:, :, 1], img_res[:, :, 2], alpha_artificiale])

    h_sfondo, w_sfondo = sfondo.shape[:2]
    x_inizio = max(0, x)
    y_inizio = max(0, y)
    x_fine = min(w_sfondo, x + w)
    y_fine = min(h_sfondo, y + h)

    if x_inizio >= x_fine or y_inizio >= y_fine:
        return sfondo

    png_y_inizio = y_inizio - y
    png_y_fine = png_y_inizio + (y_fine - y_inizio)
    png_x_inizio = x_inizio - x
    png_x_fine = png_x_inizio + (x_fine - x_inizio)

    img_res = img_res[png_y_inizio:png_y_fine, png_x_inizio:png_x_fine]

    bgr_asset = img_res[:, :, :3]
    alpha_mask = img_res[:, :, 3] / 255.0
    alpha_mask_3d = np.dstack([alpha_mask, alpha_mask, alpha_mask])

    roi = sfondo[y_inizio:y_fine, x_inizio:x_fine]
    combinato = (roi * (1.0 - alpha_mask_3d) + bgr_asset * alpha_mask_3d).astype(np.uint8)
    sfondo[y_inizio:y_fine, x_inizio:x_fine] = combinato
    return sfondo


def render_frame(frame, attiva_sfocatura, cappello_on, occhiali_on, barba_on, etichetta="User"):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    if attiva_sfocatura:
        blurred = cv2.GaussianBlur(frame, (95, 95), 0)
        for (x, y, w, h) in faces:
            blurred[y:y + h, x:x + w] = frame[y:y + h, x:x + w]
        frame = blurred

    for (x, y, w, h) in faces:
        # Etichetta sopra la faccia
        cv2.putText(frame, etichetta, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # --- OCCHIALI (Tasto I) ---
        if occhiali_on:
            # Allunghiamo la ROI degli occhi per sicurezza
            y_inizio_ricerca = int(y + h * 0.2)
            h_ricerca = int(h * 0.4)
            roi_gray_face = gray_frame[y_inizio_ricerca:y_inizio_ricerca + h_ricerca, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray_face, 1.1, 4, minSize=(int(w * 0.08), int(w * 0.08)))

            if len(eyes) >= 2:
                eyes = sorted(eyes, key=lambda e: e[0])
                ex1, ey1, ew1, eh1 = eyes[0]
                ex2, ey2, ew2, eh2 = eyes[-1]

                occhio_sinistro_x = x + ex1 + int(ew1 / 2)
                occhio_destro_x = x + ex2 + int(ew2 / 2)
                centro_occhi_y = y_inizio_ricerca + int((ey1 + eh1 / 2 + ey2 + eh2 / 2) / 2)

                distanza_occhi = occhio_destro_x - occhio_sinistro_x

                # Aumentato il moltiplicatore (da 2.1 a 2.45) per non farli sembrare stretti
                w_occhiali = int(distanza_occhi * 2.45)
                # Aumentato il rapporto d'aspetto (da 0.4 a 0.5) per non farli sembrare schiacciati
                h_occhiali = int(w_occhiali * 0.5)

                x_occhiali = occhio_sinistro_x - int((w_occhiali - distanza_occhi) / 2)
                y_occhiali = centro_occhi_y - int(h_occhiali / 2)

                frame = sovrapponi_png(frame, occhiali_img, x_occhiali, y_occhiali, w_occhiali, h_occhiali)
            else:
                # Fallback anatomico migliorato: occhiali più larghi e alti
                w_occhiali = int(w * 1.05)
                h_occhiali = int(w_occhiali * 0.5)
                x_occhiali = x - int((w_occhiali - w) / 2)
                y_occhiali = int(y + h * 0.35) - int(h_occhiali / 2)
                frame = sovrapponi_png(frame, occhiali_img, x_occhiali, y_occhiali, w_occhiali, h_occhiali)

        # --- CAPPELLO (Tasto U) ---
        if cappello_on:
            w_cap = int(w * 1.35)
            h_cap = int(w_cap * 0.65)
            x_cap = x - int((w_cap - w) / 2)
            y_cap = y - h_cap + int(h * 0.12)
            frame = sovrapponi_png(frame, cappello_img, x_cap, y_cap, w_cap, h_cap)

        # --- BARBA (Tasto B) ---
        if barba_on:
            # Allargata la barba (da 1.05 a 1.25) per coprire bene i lati del viso (zigomi e mascella)
            w_barba = int(w * 1.30)
            # Aumentata l'altezza proporzionale (da 0.65 a 0.8) per evitare l'effetto schiacciato
            h_barba = int(w_barba * 0.9)

            x_barba = x - int((w_barba - w) / 2)
            # Abbassato l'ancoraggio (dal 58% al 68% dell'altezza del viso) per spostarla sotto il naso/bocca, verso il mento
            y_barba = y + int(h * 0.30)

            frame = sovrapponi_png(frame, barba_img, x_barba, y_barba, w_barba, h_barba)

    return frame, len(faces)