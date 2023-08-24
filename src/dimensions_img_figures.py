import cv2
import imutils
import numpy as np
from imutils import contours
from imutils import perspective
from scipy.spatial import distance as dist

class DimensionsImgFigures:
  def __init__(self, pathToImage, widthReference, output_path):
    try:
      self.image = cv2.imread(pathToImage)
      self.widthReference = widthReference
      self.output_path = output_path
    except Exception as e:
      print(e)

  def start_analyze(self):
    try:
      self._prepare_image_to_find_edges()
      self._get_contours()
      self._draw_measures_in_image()
    except Exception as e:
      print(e)

  def _prepare_image_to_find_edges(self):
    """
    Prepara la imagen para encontrar bordes mediante un proceso de filtrado y detección de bordes.

    Args:
        image (numpy.ndarray): Imagen de entrada en formato NumPy array.

    Returns:
        numpy.ndarray: Imagen con bordes detectados.
    """
    gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    edge = cv2.Canny(gray, 50, 100)
    edge = cv2.dilate(edge, None, iterations=1)
    edge = cv2.erode(edge, None, iterations=1)
    self.edges = edge

  def _get_contours(self):
    """
    Encuentra y ordena los contornos en la imagen.

    Args:
        edges (numpy.ndarray): Imagen con bordes detectados.

    Returns:
        list: Lista de contornos ordenados.
    """
    cnts = cv2.findContours(self.edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    (cnts, _) = contours.sort_contours(cnts)
    self.contours = cnts

  def _draw_measures_in_image(self):
    """
    Dibuja las medidas de los objetos detectados en la imagen.

    Args:
        image (numpy.ndarray): Imagen image_copyinal.
        cnts (list): Lista de contornos ordenados.
        widthReference (float): Ancho de referencia para calcular la escala.
    """
    pixelsPerMetric = None
    for i, contour in enumerate(self.contours):
        if cv2.contourArea(contour) < 100:  # Ignora contornos pequeños
          continue
        image_copy = self.image.copy()
        box = self._compute_bounding_box(contour)
        cv2.drawContours(image_copy, [box.astype("int")], -1, (0, 255, 0), 2)
        for (x, y) in box:
            # Dibuja los puntos image_copyinales
            cv2.circle(image_copy, (int(x), int(y)), 5, (0, 0, 255), -1)
            # Calcula y dibuja los puntos medios y las líneas entre ellos
            (tl, tr, br, bl) = box
            midPoints = []
            midPoints.append(self.midpoint(tl, tr))
            midPoints.append(self.midpoint(bl, br))
            midPoints.append(self.midpoint(tl, bl))
            midPoints.append(self.midpoint(tr, br))

            for coordinates in midPoints:
              self._draw_point(image_copy, coordinates, 5, (255, 0, 0), -1)

            self._draw_line(image_copy, midPoints[0], midPoints[1], (255, 0, 255), 2)
            self._draw_line(image_copy, midPoints[2], midPoints[3], (255, 0, 255), 2)

            # Calcula la distancia euclidiana entre los puntos medios
            dA = dist.euclidean(midPoints[0], midPoints[1])
            dB = dist.euclidean( midPoints[2], midPoints[3])

        if pixelsPerMetric is None:
            pixelsPerMetric = dB / self.widthReference

        dimA = dA / pixelsPerMetric
        dimB = dB / pixelsPerMetric

        cv2.putText(image_copy, "{:.1f} cm".format(dimA),
                    (int(midPoints[0][0] - 15), int(midPoints[0][1] - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 0), 2)
        cv2.putText(image_copy, "{:.1f} cm".format(dimB),
                    (int(midPoints[3][0] + 10), int(midPoints[3][1])), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 0), 2)
        output_filename = f"{self.output_path}/output_with_measures_{i}.png"
        cv2.imwrite(output_filename, image_copy)

  def _draw_point(self, image, coordinates, rad_size, color, bold):
    cv2.circle(image, coordinates, rad_size, color, bold)

  def _draw_line(self, image, coordinatePointA, coordinatePointB, color, bold):
    cv2.line(image, (coordinatePointA), (coordinatePointB), color, bold)

  def _compute_bounding_box(self, contour):
    """
    Calcula el rectángulo delimitador de un contorno.

    Args:
        contour (numpy.ndarray): Contorno del objeto.

    Returns:
        numpy.ndarray: Puntos del rectángulo delimitador.
    """
    box = cv2.minAreaRect(contour)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    return box

  def midpoint(self, ptA, ptB):
    return (int((ptA[0] + ptB[0]) * 0.5), int((ptA[1] + ptB[1]) * 0.5))

instance = DimensionsImgFigures('./datasets/measure.png', 40.6, 'outputs')
instance.start_analyze()
