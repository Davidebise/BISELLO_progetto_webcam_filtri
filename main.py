import cv2
import datetime
import time
import os
import filters
import effects


def main():
    cap = cv2.VideoCapture(0)

    filtro_attivo = "base"
    sfocatura_attiva = False  # Stato iniziale: sfocatura spenta
    prev_time = 0

    print("Comandi: [0-3] Filtri | [F] Toggle Sfocatura | [S] Screenshot | [Q] Esci")

    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        tasto = cv2.waitKey(1) & 0xFF

        # --- GESTIONE TASTI ---
        if tasto == ord('q'):
            break
        elif tasto == ord('f'):
            sfocatura_attiva = not sfocatura_attiva  # Inverte lo stato (on/off)
        elif tasto == ord('0'):
            filtro_attivo = "Originale"
        elif tasto == ord('1'):
            filtro_attivo = "Grigio"
        elif tasto == ord('2'):
            filtro_attivo = "Negativo"
        elif tasto == ord('3'):
            filtro_attivo = "Seppia"

        # --- LOGICA EFFETTI E FILTRI ---
        # Passiamo lo stato della sfocatura alla funzione
        frame, num_faces = effects.render_frame(frame, sfocatura_attiva)

        if filtro_attivo == "Grigio":
            frame = filters.gray(frame)
        elif filtro_attivo == "Negativo":
            frame = filters.negative(frame)
        elif filtro_attivo == "Seppia":
            frame = filters.sepia(frame)

        # --- SCREENSHOT ---
        if tasto == ord('s'):
            tempo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_file = f"Screenshots/Immagine_{tempo}.jpg"
            cv2.imwrite(nome_file, frame)
            print(f"Screenshot salvato: {nome_file}")

        # --- FPS E HUD ---
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
        prev_time = curr_time

        status_blur = "ON" if sfocatura_attiva else "OFF"
        cv2.putText(frame, f"Filtro: {filtro_attivo}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Sfocatura (F): {status_blur}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(frame, f"Facce: {num_faces}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow('Webcam', frame)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()