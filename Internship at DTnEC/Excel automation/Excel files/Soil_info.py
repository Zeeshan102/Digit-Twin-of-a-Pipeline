# Import the necessary QGIS processing module
from qgis.core import QgsVectorLayer, QgsCoordinateReferenceSystem, QgsProject
import csv

# Function to set CRS for the layer
def set_crs(layer, crs):
    layer.setCrs(crs)
    if not layer.isValid():
        print(f"Error: Unable to set CRS for the layer.")
        # Handle the error appropriately

# Define the input and overlay shapefile paths
input_shapefile = 'F:/Internship at DTNEC/QGIS Pipeline/A.shp'
overlay_shapefile = 'F:/Internship at DTNEC/QGIS Pipeline/DSMW/DSMW.shp'
output_path = "F:/Internship at DTNEC/QGIS Pipeline/Excel automation/Excel files/Soil_intersected_layer/intersection_result.shp"
csv_output_path = "F:/Internship at DTNEC/QGIS Pipeline/Excel automation/Excel files/Soil_intersected_layer/result.csv"

# Set the desired CRS (EPSG:32630)
line_crs = QgsCoordinateReferenceSystem('EPSG:32630')

# Set the desired CRS (EPSG:32630)
overlay_crs = QgsCoordinateReferenceSystem('EPSG:4326')

# Load the shapefile layers
vector_layer = QgsVectorLayer(input_shapefile, "Linelayer", "ogr")
set_crs(vector_layer, line_crs)

overlay_layer = QgsVectorLayer(overlay_shapefile, "Overlay", "ogr")
set_crs(overlay_layer, overlay_crs)

# Set up the parameters for the intersection operation
parameters = {
    'INPUT': vector_layer,
    'OVERLAY': overlay_layer,
    'INPUT_FIELDS': [],
    'OVERLAY_FIELDS': [],
    'OVERLAY_FIELDS_PREFIX': '',
    'OUTPUT': output_path,
    'GRID_SIZE': None
}

# Run the intersection operation
processing.run("native:intersection", parameters)

# Access the resulting layer
result_layer = QgsVectorLayer(output_path, "Intersection Result", "ogr")

# Initialize variables to store total length and results
total_length = 0.0

# Iterate through each feature in the vector layer
for feature in vector_layer.getFeatures():
    # Access the geometry of the line feature
    geometry = feature.geometry()

    # Calculate the length of the MultiLineString with up to 2 decimal places
    total_length = round(geometry.length(), 2)

results = []

# Iterate through each feature in the result layer
for feature in result_layer.getFeatures():
    # Extract relevant attributes
    soil_type = feature['DOMSOI']
    
    # Calculate the length of the intersected portion
    intersected_length = round(feature.geometry().length(), 2)
    
    # Calculate the percentage
    percentage = round((intersected_length / total_length) * 100, 2)
    
    # Append the results to the list
    results.append([soil_type, intersected_length, percentage])

# Write the results to a CSV file
with open(csv_output_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Soil_Type', 'Intersected_Length', 'Percentage'])  # Write headers
    csv_writer.writerows(results)  # Write data rows

print(f'Results are saved to: {csv_output_path}')
