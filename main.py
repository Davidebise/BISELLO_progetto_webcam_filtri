import cv2
import datetime
import time
import os
import filters
import effects


def main():
    cap = cv2.VideoCapture(0)

    if not os.path.exists("Screenshots"):
        os.makedirs("Screenshots")

    filtro_attivo = "Originale"
    sfocatura_attiva = False

    # Stati singoli per ogni accessorio
    cappello_attivo = False
    occhiali_attivi = False
    barba_attiva = False

    nome_etichetta = "Player 1"
    prev_time = 0

    print("--- COMANDI DISPONIBILI ---")
    print("[0] Originale | [1] Grigio    | [2] Negativo | [3] Seppia")
    print("[4] Cartoon   | [5] Termico   | [6] Pixelate | [7] Vignetta")
    print("[F] Sfocatura | [U] Cappello  | [I] Occhiali | [B] Barba")
    print("[S] Screenshot | [Q] Esci")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        tasto = cv2.waitKey(1) & 0xFF

        # --- GESTIONE TASTI ---
        if tasto == ord('q'):
            break
        elif tasto == ord('f'):
            sfocatura_attiva = not sfocatura_attiva
        elif tasto == ord('u'):
            cappello_attivo = not cappello_attivo
        elif tasto == ord('i'):
            occhiali_attivi = not occhiali_attivi
        elif tasto == ord('b'):
            barba_attiva = not barba_attiva
        elif tasto == ord('0'):
            filtro_attivo = "Originale"
        elif tasto == ord('1'):
            filtro_attivo = "Grigio"
        elif tasto == ord('2'):
            filtro_attivo = "Negativo"
        elif tasto == ord('3'):
            filtro_attivo = "Seppia"
        elif tasto == ord('4'):
            filtro_attivo = "Cartoon"
        elif tasto == ord('5'):
            filtro_attivo = "Termico"
        elif tasto == ord('6'):
            filtro_attivo = "Pixelate"
        elif tasto == ord('7'):
            filtro_attivo = "Vignetta"

        # --- LOGICA EFFETTI E FILTRI ---
        # Passiamo i singoli booleani di attivazione ad effects
        frame, num_faces = effects.render_frame(
            frame,
            sfocatura_attiva,
            cappello_attivo,
            occhiali_attivi,
            barba_attiva,
            nome_etichetta
        )

        # Selezione del filtro attivo
        if filtro_attivo == "Grigio":
            frame = filters.gray(frame)
        elif filtro_attivo == "Negativo":
            frame = filters.negative(frame)
        elif filtro_attivo == "Seppia":
            frame = filters.sepia(frame)
        elif filtro_attivo == "Cartoon":
            frame = filters.cartoon(frame)
        elif filtro_attivo == "Termico":
            frame = filters.thermal(frame)
        elif filtro_attivo == "Pixelate":
            frame = filters.pixelate(frame)
        elif filtro_attivo == "Vignetta":
            frame = filters.vignette(frame)

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

        # Testi di stato per l'HUD grafico
        status_blur = "ON" if sfocatura_attiva else "OFF"
        status_cap = "ON" if cappello_attivo else "OFF"
        status_occhiali = "ON" if occhiali_attivi else "OFF"
        status_barba = "ON" if barba_attiva else "OFF"

        # Interfaccia grafica sul viso
        cv2.putText(frame, f"Filtro: {filtro_attivo}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Sfocatura (F): {status_blur}", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, f"Cappello (U): {status_cap}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)
        cv2.putText(frame, f"Occhiali (I): {status_occhiali}", (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0),
                    2)
        cv2.putText(frame, f"Barba (B): {status_barba}", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)
        cv2.putText(frame, f"Facce: {num_faces} | FPS: {int(fps)}", (10, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 255), 2)

        cv2.imshow('Webcam', frame)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()