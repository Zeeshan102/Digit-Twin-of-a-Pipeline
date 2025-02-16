from qgis.core import *

# Initialize QGIS application
QgsApplication.setPrefixPath("C:\\Program Files\\QGIS 3.28.15", True)  # Replace with your QGIS installation path
QgsApplication.initQgis()

# Function to set CRS for the layer
def set_crs(layer, crs):
    layer.setCrs(crs)
    if not layer.isValid():
        print(f"Error: Unable to set CRS for the layer.")
        # Handle the error appropriately

# Set the path to your shapefile
shapefile_path = "F:/Internship at DTNEC/QGIS Pipeline/A.shp"
# Set the path to your raster file
raster_path = "F:/Internship at DTNEC/QGIS Pipeline/A.tif"

# Set the desired CRS (EPSG 32630)
desired_crs = QgsCoordinateReferenceSystem('EPSG:32630')

# Load the shapefile as a vector layer
vector_layer = QgsVectorLayer(shapefile_path, "VectorLayer", "ogr")
set_crs(vector_layer, desired_crs)

# Load the raster layer
raster_layer = QgsRasterLayer(raster_path, "RasterLayer")
set_crs(raster_layer, desired_crs)

# Check if both layers loaded successfully
if not vector_layer.isValid() or vector_layer.geometryType() != QgsWkbTypes.LineGeometry or not raster_layer.isValid():
    print("Error: Please add a valid line shapefile and raster layer to the layers panel.")
else:
    # Create an empty list to store the results
    results = []

    # Get the coordinate transform for raster layer
    raster_crs = raster_layer.crs()
    transform = QgsCoordinateTransform(vector_layer.crs(), raster_crs, QgsProject.instance())

    # Iterate through each feature in the vector layer
    for feature in vector_layer.getFeatures():
        # Access the geometry of the line feature
        geometry = feature.geometry()

        # Calculate the length of the MultiLineString with up to 2 decimal places
        length = round(geometry.length(), 2)

        # Check if the geometry is MultiLineString
        if geometry.isMultipart():
            # Iterate through each part of the MultiLineString
            for part in geometry.asMultiPolyline():
                # Extract the starting and ending points from each part
                start_point = part[0]
                end_point = part[-1]

                # Transform the starting and ending points to raster layer CRS
                start_point_transformed = transform.transform(start_point.x(), start_point.y())
                end_point_transformed = transform.transform(end_point.x(), end_point.y())

                # Extract elevation values at the starting and ending points
                start_elevation = raster_layer.dataProvider().sample(QgsPointXY(start_point_transformed), 1)[0]
                end_elevation = raster_layer.dataProvider().sample(QgsPointXY(end_point_transformed), 1)[0]

                # Append the results to the list
                results.append({
                    'Length': length,
                    'StartLongitude': start_point_transformed.x(),
                    'StartLatitude': start_point_transformed.y(),
                    'EndLongitude': end_point_transformed.x(),
                    'EndLatitude': end_point_transformed.y(),
                    'StartElevation': start_elevation,
                    'EndElevation': end_elevation,
                })
        else:
            # Extract the starting and ending points directly
            start_point = geometry.asPolyline()[0]
            end_point = geometry.asPolyline()[-1]

            # Transform the starting and ending points to raster layer CRS
            start_point_transformed = transform.transform(start_point.x(), start_point.y())
            end_point_transformed = transform.transform(end_point.x(), end_point.y())

            # Append the results to the list
            results.append({
                'Length': length,
                'StartLongitude': start_point_transformed.x(),
                'StartLatitude': start_point_transformed.y(),
                'EndLongitude': end_point_transformed.x(),
                'EndLatitude': end_point_transformed.y(),
                'StartElevation': start_elevation,
                'EndElevation': end_elevation,
            })

    # Specify the path to the text file
    text_output_path = 'F:/Internship at DTNEC/QGIS Pipeline/Excel automation/Excel files/Length_Coordinates_Elevation_shapefile.txt'

    # Write the results to the text file
    with open(text_output_path, 'w') as file:
        for result in results:
            file.write(f"Length: {result['Length']}\n"
                       f"StartLongitude: {result['StartLongitude']}\nStartLatitude: {result['StartLatitude']}\n"
                       f"EndLongitude: {result['EndLongitude']}\nEndLatitude: {result['EndLatitude']}\n"
                       f"StartElevation: {result['StartElevation']}\nEndElevation: {result['EndElevation']}\n")

    print(f"Length, Coordinates, Elevation, Highest Elevation, and Highest Elevation Coordinates values appended to {text_output_path}")

# Finalize QGIS application
QgsApplication.exitQgis()