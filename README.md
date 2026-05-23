# README — Applicazione WebCam OpenCV

## Descrizione del Progetto
Questa applicazione Python utilizza la libreria OpenCV per catturare il flusso video della webcam in tempo reale e applicarvi filtri grafici o effetti di tracciamento facciale. Attraverso comandi rapidi da tastiera, l'utente può attivare filtri di colore, aggiungere elementi grafici (come cappelli o occhiali) sul proprio viso, scattare screenshot e registrare video.

---

## Requisiti di Sistema
* **Sistema Operativo:** Windows 10/11, macOS, o Linux (incluso Raspberry Pi OS).
* **Versione Python:** Python 3.8 o superiore.
* **Hardware Richiesto:** Una webcam (integrata o USB) funzionante.
* **Dipendenze Principali:** OpenCV (`opencv-python`) e NumPy.

---

## Installazione Step-by-Step

Segui questi passaggi partendo da zero per configurare l'ambiente e installare i componenti necessari.

### 1. Organizza i file del progetto
Assicurati di avere tutti i file all'interno della stessa cartella sul tuo computer con la seguente struttura:
```text
il_tuo_progetto/
│
├── main.py
├── effects.py
├── filters.py
├── cappello.png
├── occhiali.png
└── barba.png

```
### 2. Apri il terminale (o prompt dei comandi)
* **Windows:** Premi il tasto `Windows`, digita `cmd` e premi Invio.
* **macOS/Linux:** Apri l'applicazione `Terminale`.

### 3. Spostati nella cartella del progetto
Usa il comando `cd` seguito dal percorso della cartella in cui hai salvato i file. 
*Esempio:*
```bash
cd percorso/della/tua/cartella/il_tuo_progetto
```
### 4. Installa le librerie richieste
Esegui il seguente comando per installare automaticamente OpenCV e NumPy sul tuo sistema:
```bash
pip install opencv-python numpy
```
### 5. Come avviare l'applicazione
Una volta completata l'installazione, rimani nel terminale all'interno della cartella del progetto ed esegui il comando:
```
python main.py
```
(Nota: su alcuni sistemi macOS o Linux potrebbe essere necessario digitare python3 main.py)
### Filtri Colore
| Tasto | Azione | Descrizione |
| :---: | :--- | :--- |
| **0** | Originale | Rimuove tutti i filtri colore attivi e torna alla sorgente normale |
| **1** | Grigio | Converte il video in bianco e nero (scala di grigi) |
| **2** | Negativo | Inverte tutti i colori del frame creando un effetto "negativo fotografico" |
| **3** | Seppia | Applica un filtro nostalgico vintage sui toni caldi del marrone |
| **4** | Cartoon | Semplifica i colori e ricalca i contorni per un effetto stile fumetto |
| **5** | Termico | Mappa i livelli di luminosità simulando una visione a infrarossi (mappa Jet) |
| **6** | Pixelate | Riduce la risoluzione dell'immagine per un effetto stile "retro-gaming" |
| **7** | Vignetta | Scurisce progressivamente i bordi dell'inquadratura per focalizzare il centro |

### Effetti e Utility
| Tasto | Azione | Descrizione |
| :---: | :--- | :--- |
| **F** | Sfocatura | Attiva un effetto "bokeh" sfocando lo sfondo e mantenendo nitido il viso |
| **U** | Cappello | Posiziona l'adesivo del cappello sopra la testa rilevata |
| **I** | Occhiali | Posiziona l'adesivo degli occhiali sugli occhi rilevati |
| **B** | Barba | Posiziona l'adesivo della barba sul volto rilevato |
| **S** | Screenshot | Salva un'immagine istantanea (comprensiva di filtri) nella cartella `Screenshots` |
| **R** | Registra | Avvia o interrompe la registrazione di un file video MP4 nella cartella `Registrazioni` |
| **Q** | Esci | Chiude l'applicazione in modo sicuro e rilascia la webcam |