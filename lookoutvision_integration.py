import boto3
from PIL import Image

client = boto3.client('lookoutvision')

def start_project(project_name, model_version, min_inferences_units):
    init_project = client.start_model(
        ProjectName=project_name,
        ModelVersion=model_version,
        MinInferenceUnits=min_inferences_units
    )
    return init_project

def finish_project(project_name, model_version):
    terminate_project = client.stop_model(
        ProjectName=project_name,
        ModelVersion=model_version
    )
    return terminate_project
    
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

def detect_anomalies(project_name, model_version, content_type, photo):
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

#print(start_project('poc-rodetes-interno-figuras-circulos', '3', 1))
#print(detect_anomalies('poc-rodetes-interno-figuras-circulos', '3', 'image/jpeg', 'Circulo_Anomaly_9.jpg'))
#print(finish_project('poc-rodetes-interno-figuras-circulos', '3'))
