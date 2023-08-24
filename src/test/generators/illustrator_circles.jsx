// Función para generar un número aleatorio entre un rango específico
function getRandomNumber(min, max) {
  return Math.random() * (max - min) + min;
}

// Función para generar colores RGB aleatorios
function getRandomRGBColor() {
  var newRGBColor = new RGBColor();
  newRGBColor.red = Math.round(getRandomNumber(0, 255));
  newRGBColor.green = Math.round(getRandomNumber(0, 255));
  newRGBColor.blue = Math.round(getRandomNumber(0, 255));

  return newRGBColor;
}

function changeValuesColor(colorCircle, colorRect) {
  if (colorCircle.red === colorRect.red) {
      colorRect.red = colorRect.red + 30 > 255 ? colorRect.red - 30 : colorRect.red + 30;
  }
  else if (colorCircle.green === colorRect.green) {
      colorRect.green = colorRect.green + 30 > 255 ? colorRect.green - 30 : colorRect.green + 30;
  }
  else if (colorCircle.blue === colorRect.blue) {
      colorRect.blue = colorRect.blue + 30 > 255 ? colorRect.blue - 30 : colorRect.blue + 30;
  }
  return colorRect;
}

// Función para exportar un círculo en la capa "Normals" como archivo de imagen JPG
/*
function exportCircleAsJPG(folderName, fileName) {
  var doc = app.activeDocument;
  var filePath = "C:\\Users\\juanp\\OneDrive\\Escritorio\\Circulos\\" + folderName + fileName; // Ruta completa al archivo en tu escritorio

  var exportFile = new File(filePath);

  doc.exportFile(exportFile, ExportType.JPEG);
}*/

// Función para generar círculos centrados en la mitad de la mesa de trabajo con colores de contorno aleatorios en RGB y grosores aleatorios
function generateCirclesCenteredInArtboardWithRandomColorsAndThickness(
  numCirclesWithColorAndBackgroundColor,
  numCirclesWithOutColorAndWithBackgroundColor,
  numCirclesWithOutColorAndWithOutBackgroundColor,
  numCirclesWithColorAndWithOutBackgroundColor,
) {
  var doc = app.activeDocument;
  var artboard = doc.artboards[doc.artboards.getActiveArtboardIndex()];

  var artboardWidth = artboard.artboardRect[2] - artboard.artboardRect[0];
  var artboardHeight = artboard.artboardRect[1] - artboard.artboardRect[3];

  var normalsLayer = app.activeDocument.layers.add();
  normalsLayer.name = "Normals"; // Crear la capa "Normals"

  var numero_circulo = 0;
  var train_number = 1;
  var test_number = 1;

  for (var i = 0; i < numCirclesWithColorAndBackgroundColor; i++) {
      var radius = getRandomNumber(50, 500); // Tamaño aleatorio entre 50 y 500 puntos

      // Calcular las coordenadas (posición x e y) para que el círculo esté centrado en la mitad del ancho y alto del artboard
      var posX = artboard.artboardRect[0] + artboardWidth / 2;
      var posY = artboard.artboardRect[1] - artboardHeight / 2 + 200;

      // Agregar variaciones aleatorias a las coordenadas x e y
      var positionVariationX = getRandomNumber(-620, 200);
      var positionVariationY = getRandomNumber(-100, 150);
      posX += positionVariationX;
      posY += positionVariationY;

      // Crear un círculo
      var circle = app.activeDocument.activeLayer.pathItems.ellipse(posY, posX, radius, radius);
      circle.filled = false; // Desactivar el relleno del círculo
      circle.strokeWidth = getRandomNumber(1, 15); // Grosor aleatorio entre 1 y 10 puntos
      var colorCircle = getRandomRGBColor();
      circle.strokeColor = colorCircle; // Color del trazo aleatorio en RGB

      var subLayer = normalsLayer.layers.add();
      subLayer.name = "Círculo " + (numero_circulo + 1); // Nombre de la subcapa

      // Crear un rectángulo de fondo
      var rectangle = app.activeDocument.activeLayer.pathItems.rectangle(
          artboard.artboardRect[1],
          artboard.artboardRect[0],
          artboardWidth,
          artboardHeight
      );
      rectangle.filled = true;
      rectangle.stroked = false;
      var colorRect = changeValuesColor(colorCircle, getRandomRGBColor());
      rectangle.fillColor = colorRect;

      // Mover el círculo y el rectángulo a la subcapa
      rectangle.move(subLayer, ElementPlacement.PLACEATBEGINNING);
      circle.move(subLayer, ElementPlacement.PLACEATBEGINNING);
      numero_circulo += 1;/*
      if(i > 19){
          exportCircleAsJPG("train\\Normal\\", "Circulo_Normal_" + train_number + ".jpg");
          train_number += 1;
      }else {
          exportCircleAsJPG("test\\Normal\\", "Circulo_Normal_" + test_number + ".jpg");
          test_number += 1;
      }*/
  }

  for (var i = 0; i < numCirclesWithOutColorAndWithBackgroundColor; i++) {
      var radius = getRandomNumber(50, 500); // Tamaño aleatorio entre 50 y 500 puntos

      // Calcular las coordenadas (posición x e y) para que el círculo esté centrado en la mitad del ancho y alto del artboard
      var posX = artboard.artboardRect[0] + artboardWidth / 2;
      var posY = artboard.artboardRect[1] - artboardHeight / 2 + 200;

      // Agregar variaciones aleatorias a las coordenadas x e y
      var positionVariationX = getRandomNumber(-620, 200);
      var positionVariationY = getRandomNumber(-100, 150);
      posX += positionVariationX;
      posY += positionVariationY;

      // Crear un círculo
      var circle = app.activeDocument.activeLayer.pathItems.ellipse(posY, posX, radius, radius);
      circle.filled = false; // Desactivar el relleno del círculo
      circle.strokeWidth = getRandomNumber(1, 15); // Grosor aleatorio entre 1 y 10 puntos
      var color = new RGBColor();
      color.red = 0;
      color.green = 0;
      color.blue = 0;
      circle.strokeColor = color;

      var subLayer = normalsLayer.layers.add();
      subLayer.name = "Círculo " + (numero_circulo + 1); // Nombre de la subcapa

      // Crear un rectángulo de fondo
      var rectangle = app.activeDocument.activeLayer.pathItems.rectangle(
          artboard.artboardRect[1],
          artboard.artboardRect[0],
          artboardWidth,
          artboardHeight
      );
      rectangle.filled = true;
      rectangle.stroked = false;
      var colorRect = getRandomRGBColor();
      rectangle.fillColor = colorRect;

      // Mover el círculo y el rectángulo a la subcapa
      rectangle.move(subLayer, ElementPlacement.PLACEATBEGINNING);
      circle.move(subLayer, ElementPlacement.PLACEATBEGINNING);

      numero_circulo += 1;/*
      if(i > 19){
          exportCircleAsJPG("train\\Normal\\", "Circulo_Normal_" + train_number + ".jpg");
          train_number += 1;
      }else {
          exportCircleAsJPG("test\\Normal\\", "Circulo_Normal_" + test_number + ".jpg");
          test_number += 1;
      }*/
  }

  for (var i = 0; i < numCirclesWithOutColorAndWithOutBackgroundColor; i++) {
      var radius = getRandomNumber(50, 500); // Tamaño aleatorio entre 50 y 500 puntos

      // Calcular las coordenadas (posición x e y) para que el círculo esté centrado en la mitad del ancho y alto del artboard
      var posX = artboard.artboardRect[0] + artboardWidth / 2;
      var posY = artboard.artboardRect[1] - artboardHeight / 2 + 200;

      // Agregar variaciones aleatorias a las coordenadas x e y
      var positionVariationX = getRandomNumber(-620, 200);
      var positionVariationY = getRandomNumber(-100, 150);
      posX += positionVariationX;
      posY += positionVariationY;

      // Crear un círculo
      var circle = app.activeDocument.activeLayer.pathItems.ellipse(posY, posX, radius, radius);
      circle.filled = false; // Desactivar el relleno del círculo
      circle.strokeWidth = getRandomNumber(1, 15); // Grosor aleatorio entre 1 y 10 puntos
      var color = new RGBColor();
      color.red = 0;
      color.green = 0;
      color.blue = 0;
      circle.strokeColor = color;

      var subLayer = normalsLayer.layers.add();
      subLayer.name = "Círculo " + (numero_circulo + 1); // Nombre de la subcapa

      // Crear un rectángulo de fondo
      var rectangle = app.activeDocument.activeLayer.pathItems.rectangle(
          artboard.artboardRect[1],
          artboard.artboardRect[0],
          artboardWidth,
          artboardHeight
      );
      rectangle.filled = true;
      rectangle.stroked = false;
      var colorRect = new RGBColor();
      colorRect.red = 255;
      colorRect.green = 255;
      colorRect.blue = 255;
      rectangle.fillColor = colorRect;

      // Mover el círculo y el rectángulo a la subcapa
      rectangle.move(subLayer, ElementPlacement.PLACEATBEGINNING);
      circle.move(subLayer, ElementPlacement.PLACEATBEGINNING);

      numero_circulo += 1;/*
      if(i > 19){
          exportCircleAsJPG("train\\Normal\\", "Circulo_Normal_" + train_number + ".jpg");
          train_number += 1;
      }else {
          exportCircleAsJPG("test\\Normal\\", "Circulo_Normal_" + test_number + ".jpg");
          test_number += 1;
      }*/
  }

  for (var i = 0; i < numCirclesWithColorAndWithOutBackgroundColor; i++) {
      var radius = getRandomNumber(50, 500); // Tamaño aleatorio entre 50 y 500 puntos

      // Calcular las coordenadas (posición x e y) para que el círculo esté centrado en la mitad del ancho y alto del artboard
      var posX = artboard.artboardRect[0] + artboardWidth / 2;
      var posY = artboard.artboardRect[1] - artboardHeight / 2 + 200;

      // Agregar variaciones aleatorias a las coordenadas x e y
      var positionVariationX = getRandomNumber(-620, 200);
      var positionVariationY = getRandomNumber(-100, 150);
      posX += positionVariationX;
      posY += positionVariationY;

      // Crear un círculo
      var circle = app.activeDocument.activeLayer.pathItems.ellipse(posY, posX, radius, radius);
      circle.filled = false; // Desactivar el relleno del círculo
      circle.strokeWidth = getRandomNumber(1, 15); // Grosor aleatorio entre 1 y 10 puntos
      var color = getRandomRGBColor();
      circle.strokeColor = color;

      var subLayer = normalsLayer.layers.add();
      subLayer.name = "Círculo " + (numero_circulo + 1); // Nombre de la subcapa

      // Crear un rectángulo de fondo
      var rectangle = app.activeDocument.activeLayer.pathItems.rectangle(
          artboard.artboardRect[1],
          artboard.artboardRect[0],
          artboardWidth,
          artboardHeight
      );
      rectangle.filled = true;
      rectangle.stroked = false;
      var colorRect = new RGBColor();
      colorRect.red = 255;
      colorRect.green = 255;
      colorRect.blue = 255;
      rectangle.fillColor = colorRect;

      // Mover el círculo y el rectángulo a la subcapa
      rectangle.move(subLayer, ElementPlacement.PLACEATBEGINNING);
      circle.move(subLayer, ElementPlacement.PLACEATBEGINNING);

      numero_circulo += 1;/*
      if(i > 19){
          exportCircleAsJPG("train/Normal/", "Circulo_Normal_" + train_number + ".jpg");
          train_number += 1;
      }else {
          exportCircleAsJPG("test/Normal/", "Circulo_Normal_" + test_number + ".jpg");
          test_number += 1;
      }*/
  }
}

// Ejecutar la función para generar los círculos centrados en la mitad del artboard con colores de contorno aleatorios en RGB y grosores aleatorios
generateCirclesCenteredInArtboardWithRandomColorsAndThickness(40, 40, 40, 40);
