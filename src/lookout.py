import boto3
import os
from PIL import Image

client = boto3.client('lookoutvision')

"""
Detects images anomalies

Constructor params
:param model_name: model name trainned on lookout for vision.
:param image_path: image path to analyze.
:param version: model version to use
:param units: inference units to use for auto-scaling the model.
:return: two images at 'outputs/' folder if model found some anomaly.
"""
class AnalyzeImage:
  def __init__(self, model_name, image_path, version, units):
      self.output_folder = './outputs'
      self.model_name = model_name
      self.image_path = image_path
      self.model_version = version
      self.model_units = units

  def start_analyzis(self):
    try:
      self._content_type()
      self._detect_anomaly()
      self._process_response()
      self._save_img_response()
      self._mix_anomaly_original_imgs()
    except Exception as e:
      print(e)

  def _content_type(self):
    path_splitted = self.image_path.split('.')
    img_extension = path_splitted[len(path_splitted) - 1]
    self.content_type = "image/png" if img_extension == "png" else "image/jpeg"
    self.image_name = path_splitted[0]

  def _detect_anomaly(self):
    with open(self.image_path, "rb") as image:
      self.analysis_response = client.detect_anomalies(
        ProjectName = self.model_name,
        ContentType = self.content_type,
        Body = image.read(),
        ModelVersion = self.model_version
      )

  def _process_response(self):
    anomaly_rslt = self.analysis_response['DetectAnomalyResult']
    self.anomalies = anomaly_rslt.get('Anomalies')
    self.is_anomalous = anomaly_rslt['IsAnomalous']
    self.anomaly_mask = anomaly_rslt.get('AnomalyMask')
    print('Confidence: ', anomaly_rslt['Confidence'])
    print('Anomalies: ', 'Exist' if anomaly_rslt.get('Anomalies') else 'Not Found')
    print('IsAnomalous: ', 'Yes' if anomaly_rslt.get('IsAnomalous') else 'No')

  def img_extension(self):
    return self.content_type.split("/")[1]

  def _save_img_response(self):
    if(self.anomalies and self.is_anomalous and self.anomaly_mask):
      # "img/png" -> ['img', 'png'] -> 'png'
      output_path = f'{self.output_folder}/{self.image_name}_anomaly.{self.img_extension()}'
      self.output_anomaly_img_path = output_path
      with open(output_path, 'wb') as img_file:
        img_file.write(self.anomaly_mask)
        print(f'👉 Anomaly Image Generated as {output_path}')
    else:
      raise Exception('‼️ Anomaly Not Found, we can save image response')

  def convert_img_to_transparent(self, data):
    new_data_image = []
    # Cambiar píxeles blancos (fondo) a píxeles transparentes en la máscara de anomalía
    for item in data:
      if item[0] == 255 and item[1] == 255 and item[2] == 255:
        # Save with opacity full
        new_data_image.append((255, 255, 255, 0))
      else:
        new_data_image.append(item)
    return new_data_image

  def _mix_anomaly_original_imgs(self):
    original_image = Image.open(self.image_path)
    anomaly_mask = Image.open(self.output_anomaly_img_path).convert("RGBA")
    data = anomaly_mask.getdata()
    new_data_image = self.convert_img_to_transparent(data)
    anomaly_mask.putdata(new_data_image)
    mix_imgs = Image.alpha_composite(original_image.convert("RGBA"), anomaly_mask)
    output_path = f'{self.output_folder}/{self.image_name}_mixed.{self.img_extension()}'
    mix_imgs.save(output_path, self.img_extension())

  def start_model(self):
    try:
      init_project = client.start_model(
        ProjectName = self.model_name,
        ModelVersion = self.model_version,
        MinInferenceUnits = self.model_units
      )
      print(init_project)
    except Exception as e:
      print(e)

  def stop_model(self):
    try:
      response = client.stop_model(
        ProjectName = self.model_name,
        ModelVersion = self.model_version,
      )
      print(response)
    except Exception as e:
      print(e)

# Example
# instance = AnalyzeImage('poc-rodetes-interno-conos', 'test_cono.png', '1', 1)
# instance.start_model()
