import bpy
import random

# Nombre de la colección que contiene las cámaras
collection_name = "Collection"

# Lista de colores en formato RGB (0-1)
colors = [
    (1, 0, 0, 1),  # Rojo
    (0, 1, 0, 1),  # Verde
    (0, 0, 1, 1),  # Azul
    (1, 1, 0, 1),  # Amarillo
    (0, 1, 1, 1),  # Cian
    (1, 0, 1, 1),  # Magenta
]

# Obtener la colección por su nombre
collection = bpy.data.collections.get(collection_name)
fotoNumero = 183
# Verificar si la colección existe
if collection:
    # Iterar a través de los objetos en la colección
    for obj in collection.objects:
        if obj.type == 'CAMERA':
            if fotoNumero % 2 == 1:
                random_color = random.choice(colors)
                bpy.data.materials["Material 1.002"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = random_color
            # Establecer la cámara como la cámara activa
            bpy.context.scene.camera = obj
            
            # Renderizar la imagen 
            bpy.ops.render.render()
            
            # Guardar la imagen renderizada
            output_path = f"C:\\Users\\juanp\\OneDrive\\Escritorio\\Cones\\train\\anomaly\\Cono_Anomaly_{fotoNumero}.png"
            bpy.data.images['Render Result'].save_render(filepath=output_path)
            fotoNumero += 1
else:
    print("La colección no existe:", collection_name)
