# Import necessary QGIS modules
from qgis.core import QgsVectorLayer, QgsProject, QgsCoordinateReferenceSystem
from qgis.analysis import QgsNativeAlgorithms
import os

# Import processing
from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# Specify the path to the shapefile containing the pipeline route (single line)
pipeline_route_path = "F:\Internship at DTNEC\QGIS Pipeline\A.shp"

# Specify the directory containing the road shapefiles
road_shapefile_directory = "F:\Internship at DTNEC\QGIS Pipeline\Shapefile of roads\data\RoadLink"

# Load the pipeline route into QGIS
pipeline_route_layer = QgsVectorLayer(pipeline_route_path, "Pipeline Route", "ogr")

# Check if the pipeline route layer is loaded successfully
if not pipeline_route_layer.isValid():
    print("Error: Unable to load the pipeline route layer.")
else:
    # Set the CRS for the pipeline route (assuming EPSG:4326, you can change it accordingly)
    pipeline_route_layer.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))

    # Initialize a counter for the number of intersections
    num_intersections = 0

    # Iterate through each file in the road shapefile directory
    for filename in os.listdir(road_shapefile_directory):
        # Check if the file is a shapefile
        if filename.lower().endswith(".shp"):
            # Create the full path to the road shapefile
            road_shapefile_path = os.path.join(road_shapefile_directory, filename)

            # Load the road shapefile into QGIS
            road_layer = QgsVectorLayer(road_shapefile_path, filename[:-4], "ogr")

            # Check if the road layer is loaded successfully
            if not road_layer.isValid():
                print(f"Error: Unable to load the road layer {road_shapefile}")
            else:
                # Set the CRS for the road shapefile (assuming EPSG:4326, you can change it accordingly)
                road_layer.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))

                # Use processing algorithm to find the intersections
                result = processing.run("native:intersection", {'INPUT':pipeline_route_layer, 'OVERLAY':road_layer, 'OUTPUT':'memory:'})
                intersection_result = result['OUTPUT'].featureCount()

                # Increment the counter by the number of intersections
                num_intersections += intersection_result

                # Store the result in a text file
                result_file_path = "F:\Internship at DTNEC\QGIS Pipeline\Excel automation\Excel files\Roads.txt"
                with open(result_file_path, "w") as result_file:
                        result_file.write(str(num_intersections))

    # Print the total number of intersections
    print(f"Total number of intersections: {num_intersections}")


