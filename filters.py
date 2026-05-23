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


def cartoon(frame):
    h, w = frame.shape[:2]

    # Sottocampionamento per preservare gli FPS (riduciamo a 1/2)
    img_small = cv2.resize(frame, (w // 2, h // 2), interpolation=cv2.INTER_LINEAR)

    # Applichiamo il filtro bilaterale sulla versione piccola
    color_small = img_small
    for _ in range(2):
        color_small = cv2.bilateralFilter(color_small, d=9, sigmaColor=75, sigmaSpace=75)

    # Riportiamo alle dimensioni originali
    color = cv2.resize(color_small, (w, h), interpolation=cv2.INTER_LINEAR)

    # Rilevamento dei bordi (passaggio in scala di grigi rapido)
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray_img, 5)
    edges = cv2.Canny(gray_blur, threshold1=50, threshold2=130)

    # Inversione e sovrapposizione bordi neri
    edges_inv = cv2.bitwise_not(edges)
    edges_bgr = cv2.cvtColor(edges_inv, cv2.COLOR_GRAY2BGR)

    return cv2.bitwise_and(color, edges_bgr)


def thermal(frame):
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.applyColorMap(gray_img, cv2.COLORMAP_JET)


def pixelate(frame, pixel_size=16):
    h, w = frame.shape[:2]
    if pixel_size < 1:
        pixel_size = 1
    nw, nh = max(1, w // pixel_size), max(1, h // pixel_size)
    low_res = cv2.resize(frame, (nw, nh), interpolation=cv2.INTER_NEAREST)
    return cv2.resize(low_res, (w, h), interpolation=cv2.INTER_NEAREST)


def vignette(frame):
    h, w = frame.shape[:2]

    # Usiamo un raggio più ampio per non scurire il centro dell'inquadratura
    kernel_x = cv2.getGaussianKernel(w, w / 1.5)
    kernel_y = cv2.getGaussianKernel(h, h / 1.5)
    mask_2d = kernel_y * kernel_x.T

    # Normalizzazione protetta
    mask_max = mask_2d.max()
    if mask_max > 0:
        mask_2d = mask_2d / mask_max

    # Rendiamo l'effetto meno aggressivo al centro alzando la luminosità di base della maschera
    mask_2d = 0.3 + 0.7 * mask_2d

    mask_3d = np.dstack([mask_2d, mask_2d, mask_2d])
    return np.clip(frame * mask_3d, 0, 255).astype(np.uint8)