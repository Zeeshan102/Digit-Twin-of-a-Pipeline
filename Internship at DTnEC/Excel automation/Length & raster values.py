from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsProject, QgsWkbTypes, QgsCoordinateTransform, QgsPointXY

# Set the path to your shapefile and raster file
shapefile_path = "F:/Internship at DTNEC/QGIS Pipeline/A.shp"
raster_path = "F:/Internship at DTNEC/QGIS Pipeline/A.tif"  # Replace with the actual path to your raster file


# Load the shapefile as a vector layer
layer = QgsVectorLayer(shapefile_path, "LineLayer", "ogr")

# Load the raster layer
raster_layer = QgsRasterLayer(raster_path, "RasterLayer")

# Check if both layers loaded successfully
if not layer.isValid() or layer.geometryType() != QgsWkbTypes.LineGeometry or not raster_layer.isValid():
    print("Error: Please add a valid line shapefile and raster layer to the layers panel.")
else:
    # Create an empty list to store the results
    results = []

    # Get the coordinate transform for raster layer
    raster_crs = raster_layer.crs()
    transform = QgsCoordinateTransform(layer.crs(), raster_crs, QgsProject.instance())

    # Iterate through each feature in the layer
    for feature in layer.getFeatures():
        # Access the geometry of the line feature
        geometry = feature.geometry()

        # Calculate the length of the line feature in meters with two decimal digits
        length = round(geometry.length(), 2)

        # Print the length
        print(f"Length of Line Feature {feature.id()}: {length} meters")

        # Extract the starting and ending points
        if geometry.isMultipart():
            start_point = geometry.asMultiPolyline()[0][0]
            end_point = geometry.asMultiPolyline()[-1][-1]
        else:
            start_point = geometry.asPolyline()[0]
            end_point = geometry.asPolyline()[-1]

        # Transform the starting and ending points to raster layer CRS
        start_point = transform.transform(start_point.x(), start_point.y())
        end_point = transform.transform(end_point.x(), end_point.y())

        # Extract raster values at starting and ending points
        start_value = raster_layer.dataProvider().sample(QgsPointXY(start_point), 1)[0]
        end_value = raster_layer.dataProvider().sample(QgsPointXY(end_point), 1)[0]

        # Append the results to the list
        results.extend([length, start_value, end_value])

    # Specify the path to the output text file
    output_text_path = 'F:\Internship at DTNEC\QGIS Pipeline\Excel automation\Length & raster values.txt'

    # Save the data to the text file
    with open(output_text_path, 'w') as output_file:
        for value in results:
            output_file.write(f"{value}\n")

    print(f"Length, starting point raster value, and ending point raster value saved to {output_text_path}")


