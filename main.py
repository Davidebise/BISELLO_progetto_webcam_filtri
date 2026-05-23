import cv2
import datetime
import time
import os
import filters
import effects


def main():
    # Inizializzazione della webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Errore: Impossibile accedere alla webcam.")
        return

    # Creazione delle cartelle di output se non esistono
    if not os.path.exists("Screenshots"):
        os.makedirs("Screenshots")
    if not os.path.exists("Registrazioni"):
        os.makedirs("Registrazioni")

    # Stati dell'applicazione
    filtro_attivo = "Originale"
    sfocatura_attiva = False
    cappello_attivo = False
    occhiali_attivi = False
    barba_attiva = False

    # Stati per la registrazione video
    registrazione_attiva = False
    video_writer = None

    nome_etichetta = "Player 1"
    prev_time = time.time()

    print("--- COMANDI DISPONIBILI ---")
    print("[0] Originale | [1] Grigio    | [2] Negativo | [3] Seppia")
    print("[4] Cartoon   | [5] Termico   | [6] Pixelate | [7] Vignetta")
    print("[F] Sfocatura | [U] Cappello  | [I] Occhiali | [B] Barba")
    print("[S] Screenshot | [R] Registra  | [Q] Esci")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Errore: Impossibile ricevere i frame dalla webcam.")
            break

        # Modalità specchio (selfie mode)
        frame = cv2.flip(frame, 1)
        h_frame, w_frame = frame.shape[:2]

        # Cattura del tasto premuto
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

        # Gestione Avvio/Arresto Registrazione Video (Tasto R)
        elif tasto == ord('r'):
            registrazione_attiva = not registrazione_attiva
            if registrazione_attiva:
                tempo_video = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_video = f"Registrazioni/Video_{tempo_video}.mp4"
                # Usiamo il codec mp4v, standard e ampiamente supportato su OpenCV desktop
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                # Impostiamo 20 FPS fissi come target del file di output
                video_writer = cv2.VideoWriter(nome_video, fourcc, 20.0, (w_frame, h_frame))
                print(f"Registrazione avviata: {nome_video}")
            else:
                if video_writer is not None:
                    video_writer.release()
                    video_writer = None
                print("Registrazione salvata e conclusa.")

        # --- LOGICA EFFETTI E TRACCIAMENTO VISO ---
        frame, num_faces = effects.render_frame(
            frame,
            sfocatura_attiva,
            cappello_attivo,
            occhiali_attivi,
            barba_attiva,
            nome_etichetta
        )

        # --- SELEZIONE E APPLICAZIONE FILTRO COLORE ---
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

        # --- DISEGNO HUD SUPERIORE ED INDICATORE REGISTRAZIONE ---
        curr_time = time.time()
        differenza = curr_time - prev_time
        fps = 1 / differenza if differenza > 0 else 0
        prev_time = curr_time

        # Testi informativi standard nell'angolo superiore sinistro
        cv2.putText(frame, f"Filtro: {filtro_attivo}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Facce: {num_faces} | FPS: {int(fps)}", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 255), 2)

        # Se stiamo registrando, disegna un pallino rosso lampeggiante (basato sui millisecondi correnti)
        if registrazione_attiva:
            cv2.putText(frame, "REC", (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            if int(time.time() * 2) % 2 == 0:
                cv2.circle(frame, (65, 78), 7, (0, 0, 255), -1)

        # --- CREAZIONE E COSTRUZIONE DELLA BARRA IN BASSO (STATUS BAR) ---
        # Creiamo un rettangolo nero solido alto 40 pixel in fondo al frame
        altezza_barra = 40
        barra_inferiore = np.zeros((altezza_barra, w_frame, 3), dtype=np.uint8)

        # Costruiamo la stringa degli effetti attivi
        attivi = []
        if sfocatura_attiva: attivi.append("SFOCATURA")
        if cappello_attivo: attivi.append("CAPPELLO")
        if occhiali_attivi: attivi.append("OCCHIALI")
        if barba_attiva: attivi.append("BARBA")
        if filtro_attivo != "Originale": attivi.append(filtro_attivo.upper())

        testo_barra = "EFFETTI ATTIVI: " + (" + ".join(attivi) if attivi else "NESSUNO")

        # Scriviamo il testo sulla barra nera creata separatamente
        cv2.putText(barra_inferiore, testo_barra, (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
                    cv2.LINE_AA)

        # Sovrapponiamo la barra nera negli ultimi 40 pixel in basso dell'immagine finale
        frame[h_frame - altezza_barra: h_frame, 0: w_frame] = barra_inferiore

        # --- SCRITTURA DEL FRAME SUL FILE VIDEO (Se la registrazione è attiva) ---
        if registrazione_attiva and video_writer is not None:
            video_writer.write(frame)

        # --- GESTIONE SCREENSHOT ---
        # Salva il frame completo, inclusa la barra in basso appena applicata
        if tasto == ord('s'):
            tempo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_file = f"Screenshots/Immagine_{tempo}.jpg"
            cv2.imwrite(nome_file, frame)
            print(f"Screenshot salvato con successo: {nome_file}")

        # Mostra l'applicazione finale a schermo
        cv2.imshow('Webcam Application', frame)

    # --- CHIUSURA ACCURATA E RILASCIO RISORSE ---
    if video_writer is not None:
        video_writer.release()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    import numpy as np  # Necessario qui per la creazione della barra nera tramite array NumPy

    main()