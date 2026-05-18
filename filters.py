import cv2
import numpy as np


def gray(frame):
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)


def negative(frame):
    return cv2.bitwise_not(frame)


def sepia(frame):
    img_sepia = cv2.transform(frame, np.matrix([[0.272, 0.534, 0.131],
                                                [0.349, 0.686, 0.168],
                                                [0.393, 0.769, 0.189]]))
    return cv2.convertScaleAbs(img_sepia)


# --- NUOVI FILTRI ---

def cartoon(frame):
    # 1. Riduzione dei colori con Bilateral Filter (ripetuto 2 volte per non distruggere i FPS)
    color = frame
    for _ in range(2):
        color = cv2.bilateralFilter(color, d=9, sigmaColor=75, sigmaSpace=75)

    # 2. Rilevamento dei bordi su scala di grigi
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray_img, 7)
    edges = cv2.Canny(gray_blur, threshold1=50, threshold2=150)

    # 3. Inversione della maschera dei bordi (bordi neri su sfondo bianco)
    edges_inv = cv2.bitwise_not(edges)
    edges_bgr = cv2.cvtColor(edges_inv, cv2.COLOR_GRAY2BGR)

    # 4. Combinazione dei colori appiattiti con i bordi neri
    return cv2.bitwise_and(color, edges_bgr)


def thermal(frame):
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Applica la mappa di colore (COLORMAP_JET o COLORMAP_INFERNO)
    return cv2.applyColorMap(gray_img, cv2.COLORMAP_JET)


def pixelate(frame, pixel_size=16):
    # Evita divisioni per zero se la dimensione del pixel è errata
    h, w = frame.shape[:2]
    if pixel_size < 1:
        pixel_size = 1

    # Calcola le dimensioni ridotte
    nw, nh = max(1, w // pixel_size), max(1, h // pixel_size)

    # Rimpicciolisce e ri-ingrandisce con interpolazione NEAREST
    low_res = cv2.resize(frame, (nw, nh), interpolation=cv2.INTER_NEAREST)
    return cv2.resize(low_res, (w, h), interpolation=cv2.INTER_NEAREST)


def vignette(frame):
    h, w = frame.shape[:2]

    # Genera le matrici gaussiane per i due assi
    kernel_x = cv2.getGaussianKernel(w, w / 2)
    kernel_y = cv2.getGaussianKernel(h, h / 2)

    # Crea la maschera 2D combinando i due vettori
    mask_2d = kernel_y * kernel_x.T

    # Normalizza la maschera in modo che il centro sia vicino a 1.0
    mask_2d = mask_2d / mask_2d.max()

    # Estende la maschera a 3 canali (BGR)
    mask_3d = np.dstack([mask_2d, mask_2d, mask_2d])

    # Applica la maschera moltiplicando e riportando a uint8 senza perdere info
    vignette_frame = np.uint8(frame * mask_3d)
    return vignette_frame