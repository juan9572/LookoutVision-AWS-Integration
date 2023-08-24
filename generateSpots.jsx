// Función para generar un número aleatorio entre un rango específico
function getRandomNumber(min, max) {
    return Math.random() * (max - min) + min;
}

// Función para generar una forma de mancha irregular
function createRandomBlob(x, y, size) {
    var doc = app.activeDocument;
    var blob = doc.pathItems.add();
    blob.stroked = false; // Sin contorno
    blob.filled = true; // Con relleno

    var points = [];
    var numPoints = Math.floor(getRandomNumber(6, 20)); // Número de puntos de control
    var angleIncrement = (2 * Math.PI) / numPoints;

    for (var i = 0; i < numPoints; i++) {
        var angle = i * angleIncrement;
        var radius = getRandomNumber(size * 0.3, size * 1.5); // Radio aleatorio
        var pointX = x + radius * Math.cos(angle);
        var pointY = y + radius * Math.sin(angle);
        points.push([pointX, pointY]);
    }

    blob.setEntirePath(points);
    return blob;
}

// Función para exportar una capa como archivo de imagen JPG
function exportCircleAsJPG(folderName, fileName) {
    var doc = app.activeDocument;
    var filePath = "C:\\Users\\juanp\\OneDrive\\Escritorio\\Zones\\" + folderName + fileName; // Ruta completa al archivo en tu escritorio
    var exportFile = new File(filePath);
    doc.exportFile(exportFile, ExportType.JPEG);
}

// Función para generar manchas en la capa "Anomaly" con formas irregulares
function generateSpots(
    numberSpots,
    numberNormals,
) {
    var doc = app.activeDocument;
    var artboard = doc.artboards[doc.artboards.getActiveArtboardIndex()];

    var artboardWidth = artboard.artboardRect[2] - artboard.artboardRect[0];
    var artboardHeight = artboard.artboardRect[1] - artboard.artboardRect[3];

    /*for (var i = 0; i < numberNormals; i++) {
        exportCircleAsJPG("train\\Normal\\", "Zone_Normal_" + (i + 1) + ".jpg");
        exportCircleAsJPG("test\\Normal\\", "Zone_Normal_" + (i + 1) + ".jpg");
    }*/

    var listOfFigures = [];

    for (var i = 101; i < numberSpots; i++) {
        var posX = artboard.artboardRect[0] + artboardWidth / 2;
        var posY = artboard.artboardRect[1] - artboardHeight / 2;

        var positionVariationX = getRandomNumber(-500, 500);
        var positionVariationY = getRandomNumber(-100, 100);
        posX += positionVariationX;
        posY += positionVariationY;

        var spotSize = getRandomNumber(getRandomNumber(70, 350), getRandomNumber(70, 350)); // Tamaño de la mancha
        var blob = createRandomBlob(posX, posY, spotSize);
        var newRGBColor = new RGBColor();
        newRGBColor.red = Math.round(getRandomNumber(0, 255));
        newRGBColor.green = Math.round(getRandomNumber(0, 255));
        newRGBColor.blue = Math.round(getRandomNumber(0, 255));
        blob.fillColor = newRGBColor;

        var rectangle = app.activeDocument.activeLayer.pathItems.rectangle(
            artboard.artboardRect[1],
            artboard.artboardRect[0],
            artboardWidth,
            artboardHeight
        );
        rectangle.filled = true;
        rectangle.stroked = false;
        newRGBColor.red = 255;
        newRGBColor.green = 255;
        newRGBColor.blue = 255;
        rectangle.fillColor = newRGBColor;

        var spotLayer = app.activeDocument.layers.add();
        spotLayer.name = "Spot_" + i; // Crear una capa individual para cada mancha
        rectangle.move(spotLayer, ElementPlacement.PLACEATBEGINNING);
        blob.move(spotLayer, ElementPlacement.PLACEATBEGINNING); // Mover la mancha a la capa individual
        exportCircleAsJPG("test\\anomaly\\", "Zone_Anomaly_" + i + ".jpg");
    }
}

generateSpots(200, 100);

