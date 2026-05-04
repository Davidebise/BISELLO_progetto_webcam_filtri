import cv2
import datetime
import numpy as np
import filters
import effects
import ui


def main():
    cap = cv2.VideoCapture(0)

    filtro_attivo = 0  #salva i filtri
    save_frame = False #mi serve perchè cosi salva le foto coi filtri applicati

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        tasto = cv2.waitKey(1) & 0xFF

        if tasto == ord('q'):
            break
        elif tasto == ord('1'):
            filtro_attivo = 1
        elif tasto == ord('0'):
            filtro_attivo = 0
        elif tasto == ord('s'):
            save_frame = True

        if filtro_attivo == 1:
            frame = filters.gray(frame)

        if save_frame:
            tempo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_file = f"Screenshots/Immagine_{tempo}.png"
            cv2.imwrite(nome_file, frame)
            print(f"Screenshot filtrato salvato: {nome_file}")
            save_frame = False

        cv2.imshow('Webcam', frame)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

