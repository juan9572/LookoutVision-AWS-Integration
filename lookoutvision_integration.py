import os
import boto3
from PIL import Image
import numpy as np #n
import cv2 #n

client = boto3.client('lookoutvision')

def start_individual_project(project_name, model_version, min_inferences_units):
    init_project = client.start_model(
        ProjectName=project_name,
        ModelVersion=model_version,
        MinInferenceUnits=min_inferences_units
    )
    return init_project

def start_projects(info_projects):
    for project in info_projects:
        response_start = start_individual_project(project['name'], project['version'], project['units'])
        print(response_start)

def finish_individual_project(project_name, model_version):
    terminate_project = client.stop_model(
        ProjectName=project_name,
        ModelVersion=model_version
    )
    return terminate_project
    
def finish_projects(info_projects):
    for project in info_projects:
        response_finish = finish_individual_project(project['name'], project['version'])
        print(response_finish)
    
def save_binary_data_as_image(binary_data, output_path):
    try:
        with open(output_path, 'wb') as img_file:
            img_file.write(binary_data)
    except Exception as e:
        print("Error al decodificar los datos binarios o guardar la imagen:", e)
        
def overlay_anomaly_mask(original_image_path, anomaly_mask_path, output_path):
    try:
        original_image = Image.open(original_image_path)
        anomaly_mask = Image.open(anomaly_mask_path).convert("RGBA")
        data = anomaly_mask.getdata()
        new_data = []
        for item in data: # Cambiar píxeles blancos (fondo) a píxeles transparentes en la máscara de anomalía
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                new_data.append((255, 255, 255, 0))  # Píxel transparente
            else:
                new_data.append(item)
        anomaly_mask.putdata(new_data)
        overlaid_image = Image.alpha_composite(original_image.convert("RGBA"), anomaly_mask)
        overlaid_image.save(output_path, "PNG")
    except Exception as e:
        print("Error al superponer la máscara de anomalía:", e)
        
def get_content_type_by_photo(photo):
    image_extension = os.path.splitext(photo)[1]
    content_type = "image/png" if image_extension == "png" else "image/jpeg"
    return content_type

def detect_zone_anomaly(project_name, model_version, content_type, photo):
    with open(photo, "rb") as image:
        response = client.detect_anomalies(
            ProjectName=project_name,
            ContentType=content_type,
            Body=image.read(),
            ModelVersion=model_version
        )
        response['DetectAnomalyResult'].pop('AnomalyMask')
    return response['DetectAnomalyResult']
    
def detect_type_anomaly(project_name, model_version, content_type, photo):
    with open(photo, "rb") as image:
        response = client.detect_anomalies(
            ProjectName=project_name,
            ContentType=content_type,
            Body=image.read(),
            ModelVersion=model_version
        )
        if(response['DetectAnomalyResult']['IsAnomalous']): #Si se detecto una anomalía en la imagen
            save_binary_data_as_image(response['DetectAnomalyResult']['AnomalyMask'], "anomaly_mask.png")# Guardamos la imagen como anomaly_mask.png
            overlay_anomaly_mask(photo, "anomaly_mask.png", "output_image.png")# Superponemos la imagen original con la mascara de anomalias
        response['DetectAnomalyResult'].pop('AnomalyMask') # Retornamos los demás datos sin el AnomalyMask
    return response['DetectAnomalyResult']

def detect_anomalies(info_projects, photo):
    content_type = get_content_type_by_photo(photo)
    info = info_projects[0]
    type_anomaly = detect_type_anomaly(info['name'], info['version'], content_type, photo)
    '''if type_anomaly['DetectAnomalyResult']['IsAnomalous']:
        info = info_projects[1]
        photo = type_anomaly['output_image']
        content_type = get_content_type_by_photo(photo)
        zone_anomaly = detect_zone_anomaly(info['name'], info['version'], content_type, photo)
    return """Aquí pongo el output de concatenar ambos resultados algo como:
        is_anomaly: True | False,
        type_of_anomaly: WB (WithoutBase) {list} | N/A,
        anomaly_zone: Z1 (Upper left corner) {list} | N/A,
        confidence_in_response: 0.9 * 100,
        image_with_anomaly: path_to_file | N/A
        """'''
    return type_anomaly
         
projects_models = [
    {
        'name' : 'poc-rodetes-interno-conos',
        'version' : '1',
        'units' : 1
    },
    {
        'name' : 'poc-rodetes-interno-zonas',
        'version' : '1',
        'units' : 1
    }
]

#start_projects(projects_models)
#print(detect_anomalies(projects_models, 'Cono_Anomaly_16.png'))
#finish_projects(projects_models)

mask = cv2.imread('anomaly_mask.png') #n
mask_copy = mask.copy()
gris = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
gauss = cv2.GaussianBlur(gris, (5,5), 0)
canny = cv2.Canny(gauss, 50, 150)
contours, _ = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #n

positions = {'Z1' : 0,'Z2' : 0,'Z3' : 0,'Z4' : 0}  # n

for contour in contours:
    M = cv2.moments(contour)
    if M["m00"] == 0:
        continue
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    height, width, _ = mask.shape
    
    if cx < width / 2 and cy < height / 2:
        positions['Z1'] += 1;
    elif cx >= width / 2 and cy < height / 2:
        positions['Z2'] += 1;
    elif cx < width / 2 and cy >= height / 2:
        positions['Z3'] += 1;
    else:
        positions['Z4'] += 1;

total_edges = positions['Z1'] + positions['Z2'] + positions['Z3'] + positions['Z4']

for key, value in positions.items():
    if value != 0:
        percentage = (value / total_edges) * 100
        zone = ""
        if(key == "Z1"):
            zone = "Upper Left Corner"
        elif(key == "Z2"):
            zone = "Upper Right Corner"
        elif(key == "Z3"):
            zone = "Lower Left Corner"
        else:
            zone = "Lower Right Corner"
        print(f"El cuadrante {key} ({zone}) representa el {percentage:.2f}%")
