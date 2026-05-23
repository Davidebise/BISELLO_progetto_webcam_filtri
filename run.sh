#!/bin/bash

# Naviga nella cartella dove risiede lo script
cd "$(dirname "$0")"

echo "=== Avvio Applicazione Webcam ==="

# Verifica se Python 3 è installato
if ! command -v python3 &> /dev/null
then
    echo "Errore: Python 3 non è installato su questo sistema."
    exit 1
fi

# Esegue l'applicazione principale
python3 main.py