import pandas as pd
from qgis.core import QgsApplication, QgsVectorLayer, QgsRasterLayer, QgsProject, QgsWkbTypes, QgsCoordinateTransform

# Set the path to your shapefile
shapefile_path = "F:/Internship at DTNEC/QGIS Pipeline/A.shp"
raster_path = "F:/Internship at DTNEC/QGIS Pipeline/A.tif"  # Replace with the actual path to your raster file

# Initialize QGIS application
QgsApplication.setPrefixPath("C:/Users/Public/Desktop/QGIS 3.32.2", True)  # Set the path to your QGIS installation
qgs = QgsApplication([], False)
qgs.initQgis()

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

        # Check if the geometry is MultiLineString
        if geometry.isMultipart():
            # Extract the starting and ending points from the MultiLineString
            multi_line = geometry.asMultiPolyline()
            start_point = multi_line[0][0]
            end_point = multi_line[-1][-1]
        else:
            # Extract the starting and ending points directly
            start_point = geometry.asPolyline()[0]
            end_point = geometry.asPolyline()[-1]

        # Transform the starting and ending points to raster layer CRS
        start_point = transform.transform(start_point.x(), start_point.y())
        end_point = transform.transform(end_point.x(), end_point.y())

        # Extract raster values at starting and ending points
        start_value = raster_layer.dataProvider().sample(QgsPointXY(start_point), 1)[0]
        end_value = raster_layer.dataProvider().sample(QgsPointXY(end_point), 1)[0]

        # Append the results to the list
        results.append({
            'StartLongitude': start_point.x(),
            'StartLatitude': start_point.y(),
            'EndLongitude': end_point.x(),
            'EndLatitude': end_point.y(),
            'StartRasterValue': start_value,
            'EndRasterValue': end_value,
        })

    # Convert the new data to a pandas DataFrame
    new_data = pd.DataFrame(results)

    # Specify the path to the output text file
    output_text_path = 'F:\Internship at DTNEC\QGIS Pipeline\Excel automation\Points_with_raster_data.txt'

    # Save the data to the text file
    new_data.to_csv(output_text_path, sep='\t', index=False)

    print(f"Longitude, Latitude, and Elevation values saved to {output_text_path}")
